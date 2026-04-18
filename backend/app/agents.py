def planner_agent(idea: str) -> dict:
    return {
        "problem": f"Target problem inferred from idea: {idea[:120]}",
        "goals": [
            "Validate user pain quickly",
            "Define a narrow MVP scope",
            "Map delivery milestones",
        ],
    }


def researcher_agent(idea: str) -> dict:
    return {
        "market_signals": [
            "Growing AI-assisted product planning demand",
            "SMBs seek lower-cost strategic tooling",
        ],
        "competitors": ["Notion AI", "Jasper", "Coda AI"],
        "assumptions": [f"Demand exists for: {idea[:80]}"],
    }


def writer_agent(idea: str, plan: dict, research: dict) -> dict:
    return {
        "prd": {
            "title": f"PRD - {idea[:60]}",
            "summary": plan["problem"],
            "features": [
                "Guided idea intake",
                "Multi-agent analysis",
                "Exportable action plan",
            ],
            "milestones": [
                "Week 1: Discovery + architecture",
                "Week 2: MVP delivery",
                "Week 3: Feedback and iteration",
            ],
            "risks": research["assumptions"],
        }
    }


def reviewer_agent(prd_bundle: dict) -> dict:
    prd = prd_bundle["prd"]
    checks = {
        "has_title": bool(prd.get("title")),
        "has_features": bool(prd.get("features")),
        "has_milestones": bool(prd.get("milestones")),
    }
    prd_bundle["review"] = {
        "quality_score": 5 if all(checks.values()) else 3,
        "checks": checks,
        "next_step": "Run user interviews and prioritize top 3 features.",
    }
    return prd_bundle
