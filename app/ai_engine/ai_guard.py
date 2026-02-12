# app/ai_engine/ai_guard.py

def ai_safe_execute(ai_function, fallback_function, *args, **kwargs):
    try:
        return {
            "used_ai": True,
            "result": ai_function(*args, **kwargs)
        }
    except Exception as e:
        return {
            "used_ai": False,
            "fallback_reason": str(e),
            "result": fallback_function(*args, **kwargs)
        }
