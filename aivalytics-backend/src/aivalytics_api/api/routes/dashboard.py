from fastapi import APIRouter
from aivalytics_api.supabase_client import get_supabase

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/admin-overview")
def admin_overview():
    sb = get_supabase()

    learners = sb.table("profiles").select("id", count="exact").eq("role", "learner").execute()
    courses = sb.table("courses").select("id", count="exact").execute()
    open_tickets = sb.table("tickets").select("id", count="exact").eq("status", "open").execute()
    enrollments = sb.table("enrollments").select("progress_percent").execute()

    progress_values = [row["progress_percent"] for row in enrollments.data]
    avg_progress = round(sum(progress_values) / len(progress_values)) if progress_values else 0

    return {
        "total_learners": learners.count,
        "active_courses": courses.count,
        "open_tickets": open_tickets.count,
        "avg_course_progress": avg_progress,
    }


@router.get("/learner-overview")
def learner_overview(email: str):
    sb = get_supabase()

    profile = sb.table("profiles").select("id").eq("email", email).single().execute()
    user_id = profile.data["id"]

    enrollments = sb.table("enrollments").select("course_id, progress_percent").eq("user_id", user_id).execute()
    course_ids = [e["course_id"] for e in enrollments.data]
    avg_progress = (
        round(sum(e["progress_percent"] for e in enrollments.data) / len(enrollments.data))
        if enrollments.data else 0
    )

    sessions_completed = (
        sb.table("session_progress")
        .select("id", count="exact")
        .eq("user_id", user_id)
        .eq("watched", True)
        .execute()
    )

    live_sessions = (
        sb.table("sessions")
        .select("id", count="exact")
        .in_("course_id", course_ids if course_ids else ["00000000-0000-0000-0000-000000000000"])
        .eq("type", "live")
        .execute()
    )

    my_tickets = sb.table("tickets").select("id, status").eq("learner_id", user_id).execute()
    tickets_resolved = len([t for t in my_tickets.data if t["status"] == "closed"])

    return {
        "courses_enrolled": len(enrollments.data),
        "sessions_completed": sessions_completed.count,
        "live_sessions": live_sessions.count,
        "support_tickets": len(my_tickets.data),
        "tickets_resolved": tickets_resolved,
        "avg_course_progress": avg_progress,
    }