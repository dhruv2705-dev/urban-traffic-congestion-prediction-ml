"""
Bangalore Traffic & Infrastructure Intelligence Chatbot
Domain-specific chatbot STRICTLY bound to Bangalore traffic,
congestion prediction, and infrastructure planning.

This chatbot:
  - Only answers Bangalore traffic and infrastructure questions
  - Provides location-specific, non-repetitive answers
  - Uses formal, planning-oriented language
  - Supports English and Hindi queries
  - References area-specific physical profiles for infrastructure decisions
"""

from datetime import datetime


# ================== AREA PROFILES (for infrastructure reasoning) ==================
AREA_PROFILES = {
    "koramangala": {
        "name": "Koramangala",
        "type": "Mixed Dense (Commercial + Residential)",
        "road_width": "narrow (40-60 ft inner roads)",
        "building_density": "very high",
        "open_land": "very low",
        "key_bottleneck": "Sony World Junction",
        "key_roads": ["Sony World Junction", "Sarjapur Road"],
        "infra_recommendation": "Underpass",
        "infra_reason": (
            "Koramangala exhibits very high building density with narrow inner roads. "
            "Adjacent land is unavailable for horizontal expansion. Signal frequency is high, "
            "causing intersection delays. An underpass at Sony World Junction is recommended "
            "to eliminate surface-level signal conflicts without disrupting the urban fabric."
        ),
        "flyover_rejected": (
            "High building density limits vertical clearance for flyover ramps. "
            "An underpass provides equivalent traffic segregation with lower visual impact."
        ),
        "expansion_rejected": (
            "Open land availability is very low. Horizontal expansion would require "
            "large-scale demolition of existing commercial and residential structures."
        ),
        "congestion_cause": "Signal delays at multiple small intersections combined with dense mixed-use traffic",
        "peak_pattern": "Severe congestion during morning 8-10 AM and evening 5-8 PM due to office traffic on Sarjapur Road",
    },
    "whitefield": {
        "name": "Whitefield",
        "type": "IT Corridor",
        "road_width": "moderate (arterials wider, internal roads narrow)",
        "building_density": "moderate",
        "open_land": "moderate",
        "key_bottleneck": "Marathahalli Bridge",
        "key_roads": ["Marathahalli Bridge", "ITPL Main Road"],
        "infra_recommendation": "Road Expansion",
        "infra_reason": (
            "Whitefield has moderate building density with some undeveloped land available. "
            "Road capacity utilization is high during peak IT shift hours. "
            "Lane addition at Marathahalli Bridge corridor is recommended "
            "to increase throughput capacity."
        ),
        "flyover_rejected": (
            "The primary problem is volume overload during peak hours, not junction conflict. "
            "A flyover would be disproportionately expensive for the throughput gain achievable."
        ),
        "underpass_rejected": (
            "High water table in parts of Whitefield makes underground construction risky and costly."
        ),
        "congestion_cause": "Volume overload during IT shift changes (9-10 AM, 6-8 PM) creating single-corridor dependency",
        "peak_pattern": "Heavy congestion during IT shift hours; relatively clear during off-peak and weekends",
    },
    "indiranagar": {
        "name": "Indiranagar",
        "type": "Residential + Commercial (Upscale)",
        "road_width": "mixed (100 Feet Road wide, inner roads narrow)",
        "building_density": "high",
        "open_land": "low",
        "key_bottleneck": "CMH Road",
        "key_roads": ["100 Feet Road", "CMH Road"],
        "infra_recommendation": "Underpass",
        "infra_reason": (
            "Indiranagar has high building density with limited vacant land. "
            "Cross-traffic conflict at CMH Road intersection causes recurring delays. "
            "An underpass is recommended to eliminate surface-level conflict "
            "while preserving the residential and commercial character of the area."
        ),
        "flyover_rejected": (
            "Building proximity to road edges limits vertical ramp construction. "
            "A flyover would also disrupt the commercial character of 100 Feet Road."
        ),
        "expansion_rejected": (
            "Buildings are too close to the road. Widening would require "
            "demolition of established commercial and residential properties."
        ),
        "congestion_cause": "Cross-traffic conflict at major intersections combined with commercial activity on 100 Feet Road",
        "peak_pattern": "Congestion throughout the day due to commercial activity; peaks during evening 5-9 PM",
    },
    "m.g. road": {
        "name": "M.G. Road",
        "type": "Central Business District",
        "road_width": "wide (main arterial)",
        "building_density": "very high",
        "open_land": "none",
        "key_bottleneck": "Trinity Circle",
        "key_roads": ["Trinity Circle", "Anil Kumble Circle"],
        "infra_recommendation": "Underpass",
        "infra_reason": (
            "M.G. Road is the CBD with very high building density and zero vacant land. "
            "The Metro line runs above, occupying vertical space that prevents flyover construction. "
            "An underpass at Trinity Circle is recommended to enable traffic flow "
            "without conflicting with the elevated Metro infrastructure."
        ),
        "flyover_rejected": (
            "Metro line already occupies vertical space above road level. "
            "A second elevated structure would create structural and safety concerns."
        ),
        "expansion_rejected": (
            "Zero vacant land in the CBD. Road widening is physically impossible "
            "without demolishing high-value commercial buildings."
        ),
        "congestion_cause": "Intersection conflict at Trinity Circle and Anil Kumble Circle in the central business district",
        "peak_pattern": "Heavy congestion during business hours 9 AM-7 PM; moderate reduction on weekends",
    },
    "jayanagar": {
        "name": "Jayanagar",
        "type": "Residential (Planned Layout)",
        "road_width": "moderate (grid layout)",
        "building_density": "moderate",
        "open_land": "low (some park areas)",
        "key_bottleneck": "South End Circle",
        "key_roads": ["Jayanagar 4th Block", "South End Circle"],
        "infra_recommendation": "Road Expansion",
        "infra_reason": (
            "Jayanagar has a planned grid layout with moderate building density. "
            "Some roads can be widened with minimal displacement. "
            "Targeted road widening and junction redesign at South End Circle "
            "would improve flow efficiency."
        ),
        "flyover_rejected": (
            "Jayanagar is primarily residential. Flyover construction would cause "
            "disproportionate disruption to the residential character."
        ),
        "underpass_rejected": (
            "Dense underground utility network makes excavation high-risk. "
            "Moderate signal frequency does not justify underground construction costs."
        ),
        "congestion_cause": "Road capacity limitation at South End Circle combined with growing residential vehicle ownership",
        "peak_pattern": "Morning and evening peaks aligned with school and office timings",
    },
    "hebbal": {
        "name": "Hebbal",
        "type": "Transit Hub (Highway Junction)",
        "road_width": "wide (NH7)",
        "building_density": "moderate",
        "open_land": "moderate (near lake area)",
        "key_bottleneck": "Hebbal Flyover",
        "key_roads": ["Hebbal Flyover", "Ballari Road"],
        "infra_recommendation": "Flyover / Overbridge",
        "infra_reason": (
            "Hebbal has an existing flyover but merge and diverge points create bottlenecks. "
            "Flyover extension or additional ramp construction is recommended "
            "to distribute merge traffic across multiple points."
        ),
        "underpass_rejected": (
            "Proximity to Hebbal Lake raises the water table, making underground construction risky."
        ),
        "expansion_rejected": (
            "The primary problem is merge conflict at the flyover, not insufficient road width. "
            "Widening would not address the core junction conflict."
        ),
        "congestion_cause": "Merge and diverge conflicts at existing flyover entry/exit ramps",
        "peak_pattern": "Heavy congestion during morning inbound (8-10 AM) and evening outbound (5-8 PM) due to highway traffic",
    },
    "yeshwanthpur": {
        "name": "Yeshwanthpur",
        "type": "Industrial + Commercial",
        "road_width": "wide (industrial roads)",
        "building_density": "low",
        "open_land": "moderate (industrial plots)",
        "key_bottleneck": "Yeshwanthpur Circle",
        "key_roads": ["Yeshwanthpur Circle", "Tumkur Road"],
        "infra_recommendation": "Flyover / Overbridge",
        "infra_reason": (
            "Yeshwanthpur has a railway line crossing at Yeshwanthpur Circle. "
            "Road-rail conflict causes recurring delays. "
            "A grade-separated flyover is recommended to eliminate "
            "rail-road conflict and restore uninterrupted vehicular flow."
        ),
        "underpass_rejected": (
            "While underground construction is feasible, the existing rail infrastructure "
            "favors an overbridge solution for simpler construction and lower disruption."
        ),
        "expansion_rejected": (
            "The primary problem is rail-road conflict, not insufficient road width. "
            "Widening would not eliminate the recurring delays caused by railway crossings."
        ),
        "congestion_cause": "Railway crossing at Yeshwanthpur Circle causing periodic road closures and accumulated traffic",
        "peak_pattern": "Congestion spikes correlate with train schedules; morning and evening peaks amplified by rail delays",
    },
    "electronic city": {
        "name": "Electronic City",
        "type": "IT + Industrial Hub",
        "road_width": "moderate (elevated expressway exists)",
        "building_density": "moderate",
        "open_land": "high (peripheral area)",
        "key_bottleneck": "Silk Board Junction",
        "key_roads": ["Silk Board Junction", "Hosur Road"],
        "infra_recommendation": "Flyover / Overbridge",
        "infra_reason": (
            "Electronic City operates as an IT and industrial zone with entry/exit bottleneck "
            "at Silk Board Junction. An extended elevated corridor is recommended "
            "to bypass surface-level entry congestion."
        ),
        "underpass_rejected": (
            "Rocky terrain in parts of Electronic City increases underground construction cost significantly. "
            "Existing elevated expressway infrastructure favors vertical extension."
        ),
        "expansion_rejected": (
            "While land is available, the problem is entry/exit concentration, not lane insufficiency. "
            "An alternate elevated route addresses the root cause better than widening."
        ),
        "congestion_cause": "Entry/exit bottleneck at Silk Board Junction funneling all Electronic City traffic through a single corridor",
        "peak_pattern": "Extremely heavy during IT shift changes (9-10 AM, 6-8 PM); Silk Board is Bangalore's worst bottleneck",
    },
}

# Known area name aliases for detection
AREA_ALIASES = {
    "koramangala": "koramangala",
    "whitefield": "whitefield",
    "white field": "whitefield",
    "indiranagar": "indiranagar",
    "indira nagar": "indiranagar",
    "mg road": "m.g. road",
    "m.g. road": "m.g. road",
    "m g road": "m.g. road",
    "mahatma gandhi road": "m.g. road",
    "jayanagar": "jayanagar",
    "jaya nagar": "jayanagar",
    "hebbal": "hebbal",
    "yeshwanthpur": "yeshwanthpur",
    "yeshwantpur": "yeshwanthpur",
    "electronic city": "electronic city",
    "silk board": "electronic city",
    "silkboard": "electronic city",
    "marathahalli": "whitefield",
    "marathon halli": "whitefield",
    "sony world": "koramangala",
    "sarjapur road": "koramangala",
    "cmh road": "indiranagar",
    "100 feet road": "indiranagar",
    "trinity circle": "m.g. road",
    "south end circle": "jayanagar",
    "ballari road": "hebbal",
    "bellary road": "hebbal",
    "tumkur road": "yeshwanthpur",
    "hosur road": "electronic city",
    "outer ring road": "whitefield",
}

# Out-of-scope detection keywords
OUT_OF_SCOPE_KEYWORDS = [
    "delhi", "mumbai", "chennai", "hyderabad", "pune", "kolkata",
    "new york", "london", "tokyo", "dubai",
    "python", "java", "javascript", "code", "programming",
    "recipe", "cooking", "food",
    "movie", "song", "music", "cricket", "football", "sports",
    "politics", "election", "prime minister", "president",
    "weather", "temperature", "rain forecast",
    "stock market", "crypto", "bitcoin", "share price",
    "ai model", "chatgpt", "openai",
    "write a program", "homework", "essay", "poem", "story",
    "health", "doctor", "medicine",
]

SCOPE_MESSAGE = (
    "I am designed to answer questions related only to this "
    "Bangalore traffic and infrastructure planning project."
)


def _detect_areas(query_lower):
    """Detect mentioned Bangalore areas from query text."""
    found = []
    for alias, area_key in AREA_ALIASES.items():
        if alias in query_lower and area_key not in found:
            found.append(area_key)
    return found


def _is_out_of_scope(query_lower):
    """Check if the query is outside Bangalore traffic domain."""
    # Check if any Bangalore area is mentioned — if so, it's in-scope
    detected_areas = _detect_areas(query_lower)
    if detected_areas:
        return False

    # Check if Bangalore is explicitly mentioned
    bangalore_terms = ["bangalore", "bengaluru", "namma"]
    has_bangalore = any(bt in query_lower for bt in bangalore_terms)
    if has_bangalore:
        return False

    # Check for out-of-scope keywords
    for keyword in OUT_OF_SCOPE_KEYWORDS:
        if keyword in query_lower:
            return True

    # If no Bangalore context AND no traffic/infrastructure terms, reject
    traffic_terms = [
        "traffic", "congestion", "road", "route", "flyover",
        "underpass", "infrastructure", "jam", "signal",
        "commute", "bottleneck", "corridor",
    ]
    if not any(tt in query_lower for tt in traffic_terms):
        # Check if it's a greeting or general question
        greetings = ["hello", "hi", "hey", "help", "what can you", "kya kar"]
        if any(g in query_lower for g in greetings):
            return False
        # If no traffic context at all, might be out of scope
        # But be lenient — only reject if clearly non-traffic
        return False

    return False


def _detect_intent(query_lower):
    """Detect the intent category of the query."""
    # Infrastructure questions
    infra_keywords = [
        "flyover", "overbridge", "underpass", "road expansion", "widen",
        "bridge", "tunnel", "infrastructure", "construction", "build",
        "banana chahiye", "banana chaiye", "banao", "banana",
        "expand", "alternate road", "new road",
    ]

    # Traffic status questions
    traffic_keywords = [
        "traffic", "jam", "congestion", "busy", "rush", "crowded",
        "heavy", "clear", "flow", "kaisa", "kaise", "hoga", "hai",
        "abhi", "status", "situation", "current",
    ]

    # Route / travel questions
    route_keywords = [
        "route", "rasta", "way", "path", "go", "reach", "travel",
        "commute", "jana", "pahunchna", "se", "to", "from",
        "fastest", "shortest", "best route", "bata",
    ]

    # Time / when questions
    time_keywords = [
        "time", "when", "kab", "best time", "peak", "off peak",
        "morning", "evening", "night", "weekend", "weekday",
    ]

    # Safety questions
    safety_keywords = [
        "safe", "accident", "incident", "danger", "risky", "risk",
    ]

    # Why / reason questions
    why_keywords = [
        "why", "kyu", "kyun", "reason", "cause", "wajah",
    ]

    # Prediction questions
    predict_keywords = [
        "predict", "prediction", "forecast", "future", "tomorrow",
        "next week", "expected", "estimate",
    ]

    if any(k in query_lower for k in infra_keywords):
        return "infrastructure"
    elif any(k in query_lower for k in predict_keywords):
        return "prediction"
    elif any(k in query_lower for k in why_keywords):
        return "why"
    elif any(k in query_lower for k in route_keywords):
        return "route"
    elif any(k in query_lower for k in time_keywords):
        return "time"
    elif any(k in query_lower for k in safety_keywords):
        return "safety"
    elif any(k in query_lower for k in traffic_keywords):
        return "traffic"
    else:
        return "general"


# ================== RESPONSE GENERATORS ==================

def _respond_infrastructure(areas, traffic_df, query_lower):
    """Generate infrastructure-specific response."""
    if not areas:
        # General infrastructure question
        return (
            "**Infrastructure Planning Advisory**\n\n"
            "To provide a specific infrastructure recommendation, "
            "please mention the Bangalore area or corridor you are inquiring about.\n\n"
            "**Areas under analysis:** Koramangala, Whitefield, Indiranagar, "
            "M.G. Road, Jayanagar, Hebbal, Yeshwanthpur, Electronic City.\n\n"
            "Each location has distinct physical constraints (road width, building density, "
            "land availability, elevation) that determine the feasible infrastructure type. "
            "Please specify the area for a detailed location-specific assessment."
        )

    responses = []
    for area_key in areas:
        profile = AREA_PROFILES.get(area_key)
        if not profile:
            continue

        area_data = traffic_df[traffic_df['Area Name'] == profile['name']]
        avg_cong = area_data['Congestion Level'].mean() if len(area_data) > 0 else 0
        capacity = area_data['Road Capacity Utilization'].mean() if len(area_data) > 0 else 0

        # Check if asking about a specific infra type
        asking_flyover = any(k in query_lower for k in ["flyover", "overbridge", "bridge", "elevated"])
        asking_underpass = any(k in query_lower for k in ["underpass", "tunnel", "underground"])
        asking_expansion = any(k in query_lower for k in ["widen", "expansion", "expand", "road expansion", "lane"])

        if asking_flyover and profile["infra_recommendation"] != "Flyover / Overbridge":
            response = (
                f"**Infrastructure Assessment: {profile['name']} -- Flyover**\n\n"
                f"**Area Type:** {profile['type']}\n"
                f"**Current Congestion:** {avg_cong:.1f}%\n"
                f"**Road Capacity Utilization:** {capacity:.1f}%\n\n"
                f"**Assessment: A flyover is NOT the recommended option "
                f"for {profile['name']}.**\n\n"
                f"**Reason for rejection:** {profile['flyover_rejected']}\n\n"
                f"**Recommended alternative:** {profile['infra_recommendation']}\n\n"
                f"**Justification:** {profile['infra_reason']}"
            )
        elif asking_underpass and profile["infra_recommendation"] != "Underpass":
            response = (
                f"**Infrastructure Assessment: {profile['name']} -- Underpass**\n\n"
                f"**Area Type:** {profile['type']}\n"
                f"**Current Congestion:** {avg_cong:.1f}%\n"
                f"**Road Capacity Utilization:** {capacity:.1f}%\n\n"
                f"**Assessment: An underpass is NOT the recommended option "
                f"for {profile['name']}.**\n\n"
                f"**Reason for rejection:** {profile['underpass_rejected']}\n\n"
                f"**Recommended alternative:** {profile['infra_recommendation']}\n\n"
                f"**Justification:** {profile['infra_reason']}"
            )
        elif asking_expansion and profile["infra_recommendation"] != "Road Expansion":
            response = (
                f"**Infrastructure Assessment: {profile['name']} -- Road Expansion**\n\n"
                f"**Area Type:** {profile['type']}\n"
                f"**Current Congestion:** {avg_cong:.1f}%\n"
                f"**Road Capacity Utilization:** {capacity:.1f}%\n\n"
                f"**Assessment: Road expansion is NOT the recommended option "
                f"for {profile['name']}.**\n\n"
                f"**Reason for rejection:** {profile['expansion_rejected']}\n\n"
                f"**Recommended alternative:** {profile['infra_recommendation']}\n\n"
                f"**Justification:** {profile['infra_reason']}"
            )
        else:
            response = (
                f"**Infrastructure Assessment: {profile['name']}**\n\n"
                f"**Area Type:** {profile['type']}\n"
                f"**Road Width:** {profile['road_width']}\n"
                f"**Building Density:** {profile['building_density']}\n"
                f"**Open Land Availability:** {profile['open_land']}\n"
                f"**Key Bottleneck:** {profile['key_bottleneck']}\n"
                f"**Current Congestion:** {avg_cong:.1f}%\n"
                f"**Road Capacity Utilization:** {capacity:.1f}%\n\n"
                f"---\n\n"
                f"**Recommended Infrastructure: {profile['infra_recommendation']}**\n\n"
                f"{profile['infra_reason']}\n\n"
                f"---\n\n"
                f"**Why other options are not suitable:**\n\n"
                f"- **Flyover:** {profile['flyover_rejected']}\n"
                f"- **Road Expansion:** {profile['expansion_rejected']}\n"
                f"- **Underpass:** {profile['underpass_rejected']}"
            )

        responses.append(response)

    return "\n\n---\n\n".join(responses)


def _respond_traffic(areas, traffic_df):
    """Generate traffic status response."""
    current_hour = datetime.now().hour
    is_peak = 8 <= current_hour <= 10 or 17 <= current_hour <= 20
    current_time = datetime.now().strftime("%I:%M %p")

    if areas:
        responses = []
        for area_key in areas:
            profile = AREA_PROFILES.get(area_key)
            if not profile:
                continue

            area_data = traffic_df[traffic_df['Area Name'] == profile['name']]
            if len(area_data) == 0:
                continue

            avg_cong = area_data['Congestion Level'].mean()
            avg_speed = area_data['Average Speed'].mean()
            incidents = area_data['Incident Reports'].sum()

            if avg_cong > 70:
                severity = "CRITICAL"
            elif avg_cong > 50:
                severity = "HIGH"
            elif avg_cong > 30:
                severity = "MODERATE"
            else:
                severity = "LOW"

            response = (
                f"**Traffic Status: {profile['name']}**\n\n"
                f"**Severity:** {severity}\n"
                f"**Average Congestion:** {avg_cong:.1f}%\n"
                f"**Average Speed:** {avg_speed:.1f} km/h\n"
                f"**Incident Reports:** {incidents}\n"
                f"**Time:** {current_time} ({'Peak Hours' if is_peak else 'Off-Peak'})\n\n"
                f"**Congestion Cause:** {profile['congestion_cause']}\n\n"
                f"**Peak Pattern:** {profile['peak_pattern']}\n\n"
                f"**Key Bottleneck:** {profile['key_bottleneck']} "
                f"on {'/ '.join(profile['key_roads'])}"
            )
            responses.append(response)

        return "\n\n---\n\n".join(responses)

    else:
        # General Bangalore traffic overview
        avg_congestion = traffic_df['Congestion Level'].mean()
        avg_speed = traffic_df['Average Speed'].mean()
        area_cong = traffic_df.groupby('Area Name')['Congestion Level'].mean().sort_values()

        best_area = area_cong.index[0]
        worst_area = area_cong.index[-1]

        return (
            f"**Bangalore Traffic Overview**\n\n"
            f"**Time:** {current_time} ({'Peak Hours' if is_peak else 'Off-Peak'})\n"
            f"**City Average Congestion:** {avg_congestion:.1f}%\n"
            f"**City Average Speed:** {avg_speed:.1f} km/h\n\n"
            f"**Least Congested:** {best_area} ({area_cong.iloc[0]:.1f}%)\n"
            f"**Most Congested:** {worst_area} ({area_cong.iloc[-1]:.1f}%)\n\n"
            f"{'**Advisory:** Peak hour traffic is active. Plan travel with buffer time.' if is_peak else '**Advisory:** Off-peak conditions. Favorable for travel.'}\n\n"
            f"For area-specific analysis, mention the location name "
            f"(e.g., Koramangala, Whitefield, Silk Board)."
        )


def _respond_route(areas, traffic_df):
    """Generate route advisory response."""
    if len(areas) >= 2:
        area1 = AREA_PROFILES.get(areas[0])
        area2 = AREA_PROFILES.get(areas[1])
        if area1 and area2:
            data1 = traffic_df[traffic_df['Area Name'] == area1['name']]
            data2 = traffic_df[traffic_df['Area Name'] == area2['name']]
            cong1 = data1['Congestion Level'].mean() if len(data1) > 0 else 0
            cong2 = data2['Congestion Level'].mean() if len(data2) > 0 else 0
            avg_cong = (cong1 + cong2) / 2

            # Find best intermediate area
            all_areas = traffic_df.groupby('Area Name')['Congestion Level'].mean().sort_values()
            intermediates = [
                a for a in all_areas.index
                if a not in [area1['name'], area2['name']]
            ]

            response = (
                f"**Corridor Analysis: {area1['name']} to {area2['name']}**\n\n"
                f"**{area1['name']}:** Congestion {cong1:.1f}% | "
                f"Bottleneck: {area1['key_bottleneck']}\n"
                f"**{area2['name']}:** Congestion {cong2:.1f}% | "
                f"Bottleneck: {area2['key_bottleneck']}\n"
                f"**Corridor Average:** {avg_cong:.1f}%\n\n"
            )

            if avg_cong > 60:
                response += (
                    f"**Advisory:** This corridor exhibits elevated congestion. "
                    f"Consider routing through {intermediates[0]} to distribute traffic load.\n\n"
                )
            else:
                response += (
                    f"**Advisory:** Corridor congestion is within manageable limits. "
                    f"Direct route is recommended.\n\n"
                )

            response += (
                f"**Route visualization** is available in the User Advisory section. "
                f"Navigate to User Advisory > Interactive Route Map for detailed directions."
            )

            return response

    elif len(areas) == 1:
        profile = AREA_PROFILES.get(areas[0])
        if profile:
            area_data = traffic_df[traffic_df['Area Name'] == profile['name']]
            avg_cong = area_data['Congestion Level'].mean() if len(area_data) > 0 else 0
            all_areas = traffic_df.groupby('Area Name')['Congestion Level'].mean().sort_values()

            return (
                f"**Route Advisory from/to {profile['name']}**\n\n"
                f"**Current Congestion:** {avg_cong:.1f}%\n"
                f"**Primary Bottleneck:** {profile['key_bottleneck']}\n\n"
                f"**Recommended:** Avoid {profile['key_bottleneck']} during peak hours. "
                f"Route through {all_areas.index[0]} corridor for lower congestion.\n\n"
                f"For map-based route visualization, navigate to "
                f"User Advisory > Interactive Route Map."
            )

    return (
        "To provide route analysis, please specify the start and end locations "
        "within Bangalore (e.g., 'Koramangala to Whitefield').\n\n"
        "**Available areas:** Koramangala, Whitefield, Indiranagar, "
        "M.G. Road, Jayanagar, Hebbal, Yeshwanthpur, Electronic City."
    )


def _respond_time(areas, traffic_df):
    """Generate time-based advisory."""
    current_hour = datetime.now().hour
    is_peak = 8 <= current_hour <= 10 or 17 <= current_hour <= 20

    if areas:
        profile = AREA_PROFILES.get(areas[0])
        if profile:
            return (
                f"**Travel Timing Advisory: {profile['name']}**\n\n"
                f"**Peak Pattern:** {profile['peak_pattern']}\n\n"
                f"**Current Status:** {'Peak hours active' if is_peak else 'Off-peak period'}\n\n"
                f"**Recommended Travel Windows:**\n"
                f"- Morning: Before 7:30 AM or after 11:00 AM\n"
                f"- Evening: After 8:30 PM\n"
                f"- Optimal: Weekends and public holidays\n\n"
                f"**Specific to {profile['name']}:** "
                f"The bottleneck at {profile['key_bottleneck']} "
                f"is most severe during standard office commute hours."
            )

    # General
    best_days = traffic_df.groupby('DayOfWeek')['Congestion Level'].mean().sort_values()
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    return (
        f"**Bangalore Travel Timing Advisory**\n\n"
        f"**Current Status:** {'Peak hours -- expect delays' if is_peak else 'Off-peak -- favorable conditions'}\n\n"
        f"**Best Days for Travel:**\n"
        f"1. {day_names[best_days.index[0]]} ({best_days.iloc[0]:.1f}% avg congestion)\n"
        f"2. {day_names[best_days.index[1]]} ({best_days.iloc[1]:.1f}% avg congestion)\n\n"
        f"**Avoid:** Weekday mornings 8-10 AM and evenings 5-8 PM\n\n"
        f"For area-specific timing, mention the location name."
    )


def _respond_safety(areas, traffic_df):
    """Generate safety advisory."""
    incident_data = traffic_df.groupby('Area Name')['Incident Reports'].sum().sort_values()

    if areas:
        profile = AREA_PROFILES.get(areas[0])
        if profile:
            area_data = traffic_df[traffic_df['Area Name'] == profile['name']]
            incidents = area_data['Incident Reports'].sum() if len(area_data) > 0 else 0

            return (
                f"**Safety Assessment: {profile['name']}**\n\n"
                f"**Total Incident Reports:** {incidents}\n"
                f"**Area Type:** {profile['type']}\n"
                f"**Key Risk Point:** {profile['key_bottleneck']}\n\n"
                f"**Assessment:** "
                f"{'High incident frequency. Exercise additional caution, especially during peak hours.' if incidents > 100 else 'Moderate incident levels. Standard precautions recommended.'}\n\n"
                f"**Safest Corridor:** {incident_data.index[0]} ({incident_data.iloc[0]} incidents)"
            )

    return (
        f"**Bangalore Road Safety Overview**\n\n"
        f"**Safest Area:** {incident_data.index[0]} ({incident_data.iloc[0]} incidents)\n"
        f"**Highest Risk:** {incident_data.index[-1]} ({incident_data.iloc[-1]} incidents)\n\n"
        f"Exercise increased caution in high-congestion zones during peak hours. "
        f"For area-specific safety data, mention the location name."
    )


def _respond_why(areas, traffic_df):
    """Explain why congestion occurs at specific locations."""
    if areas:
        profile = AREA_PROFILES.get(areas[0])
        if profile:
            area_data = traffic_df[traffic_df['Area Name'] == profile['name']]
            avg_cong = area_data['Congestion Level'].mean() if len(area_data) > 0 else 0
            capacity = area_data['Road Capacity Utilization'].mean() if len(area_data) > 0 else 0

            return (
                f"**Congestion Root Cause Analysis: {profile['name']}**\n\n"
                f"**Area Type:** {profile['type']}\n"
                f"**Current Congestion:** {avg_cong:.1f}%\n"
                f"**Road Capacity Utilization:** {capacity:.1f}%\n\n"
                f"**Primary Cause:** {profile['congestion_cause']}\n\n"
                f"**Contributing Factors:**\n"
                f"- Road width: {profile['road_width']}\n"
                f"- Building density: {profile['building_density']}\n"
                f"- Open land for expansion: {profile['open_land']}\n\n"
                f"**Key Bottleneck:** {profile['key_bottleneck']}\n\n"
                f"**Peak Pattern:** {profile['peak_pattern']}"
            )

    return (
        "To provide specific congestion analysis, please mention the "
        "Bangalore area you are inquiring about (e.g., 'Why is Silk Board so congested?')."
    )


def _respond_prediction(areas, traffic_df):
    """Generate congestion prediction response."""
    if areas:
        profile = AREA_PROFILES.get(areas[0])
        if profile:
            area_data = traffic_df[traffic_df['Area Name'] == profile['name']]
            avg_cong = area_data['Congestion Level'].mean() if len(area_data) > 0 else 0
            current_hour = datetime.now().hour

            if 8 <= current_hour <= 10 or 17 <= current_hour <= 20:
                forecast = "High congestion expected to continue for the next 1-2 hours."
            elif current_hour < 8:
                forecast = "Congestion expected to increase as morning peak hours approach (8-10 AM)."
            elif 10 < current_hour < 17:
                forecast = "Moderate congestion expected. Next peak anticipated at 5 PM."
            else:
                forecast = "Congestion expected to reduce gradually over the next 1-2 hours."

            return (
                f"**Congestion Prediction: {profile['name']}**\n\n"
                f"**Historical Average:** {avg_cong:.1f}%\n"
                f"**Peak Pattern:** {profile['peak_pattern']}\n\n"
                f"**Near-term Forecast:** {forecast}\n\n"
                f"**Key Factor:** {profile['congestion_cause']}\n\n"
                f"For ML-based predictions with custom parameters, navigate to "
                f"Predict Congestion in the sidebar."
            )

    return (
        "The ML-based congestion prediction model is available in the "
        "Predict Congestion section. You can input custom parameters "
        "including area, road, weather, and time to get a prediction.\n\n"
        "For a quick forecast, mention a specific Bangalore area."
    )


def _respond_general_bangalore(traffic_df):
    """General greeting / default response for Bangalore traffic context."""
    avg_congestion = traffic_df['Congestion Level'].mean()
    area_cong = traffic_df.groupby('Area Name')['Congestion Level'].mean().sort_values()

    return (
        "**Bangalore Traffic & Infrastructure Intelligence System**\n\n"
        "This system provides analysis exclusively for Bangalore traffic "
        "corridors and infrastructure planning.\n\n"
        f"**City Overview:** Average congestion at {avg_congestion:.1f}%\n"
        f"**Most congested:** {area_cong.index[-1]} ({area_cong.iloc[-1]:.1f}%)\n"
        f"**Least congested:** {area_cong.index[0]} ({area_cong.iloc[0]:.1f}%)\n\n"
        "**You may ask about:**\n"
        "- Traffic status for specific areas\n"
        "- Infrastructure recommendations (flyover, underpass, road expansion)\n"
        "- Route analysis between two locations\n"
        "- Congestion predictions\n"
        "- Safety assessments\n\n"
        "**Example queries:**\n"
        "- \"Koramangala me flyover banana chahiye?\"\n"
        "- \"Silk Board pe underpass better rahega?\"\n"
        "- \"Whitefield to Indiranagar traffic kaisa hai?\"\n"
        "- \"Why is Hebbal so congested?\""
    )


def _generate_suggestions(intent, areas, user_role):
    """Generate context-aware follow-up suggestions based on intent and role."""
    suggestions = []
    
    if intent == "traffic":
        suggestions = [
            "Why is traffic high here?",
            "Best time to travel?",
            "Alternate route options?"
        ]
    elif intent == "infrastructure":
        if user_role == "government":
            suggestions = [
                "Why this option is recommended?",
                "What are the constraints here?",
                "What if another option is chosen?"
            ]
        else:
            suggestions = [
                "When will this be built?",
                "Will it reduce my travel time?",
                "Alternate travel paths?"
            ]
    elif intent == "route":
        suggestions = [
            "Which route is better?",
            "Expected delay?",
            "Congestion comparison with other routes?"
        ]
    elif intent == "why":
        if user_role == "government":
            suggestions = [
                "How can congestion be reduced?",
                "Any short-term solution?",
                "Long-term planning suggestion?"
            ]
        else:
            suggestions = [
                "Is it always like this?",
                "Best time to avoid this?",
                "Alternate area to travel through?"
            ]
    else:
        # General suggestions
        if user_role == "government":
            suggestions = [
                "Show city-wide congestion hotspots",
                "Analyze infrastructure gaps",
                "Check recent incident impact"
            ]
        else:
            suggestions = [
                "Current traffic in Koramangala?",
                "Best route to Whitefield?",
                "Traffic prediction for tomorrow?"
            ]
            
    return suggestions[:5] # Limit to 5


# ================== MAIN CHATBOT FUNCTION ==================
def generate_chatbot_response(user_query, traffic_df, user_role="user"):
    """
    Bangalore Traffic & Infrastructure Intelligence System.
    Domain-scoped, location-aware, non-repetitive chatbot.
    Returns a dictionary with 'content' and 'suggestions'.
    """
    query_lower = user_query.lower().strip()

    # 1. Out-of-scope check (STRICT)
    if _is_out_of_scope(query_lower):
        return {
            "content": "I am designed to answer questions related only to this Bangalore traffic and congestion prediction project.",
            "suggestions": []
        }

    # 2. Detect areas mentioned
    areas = _detect_areas(query_lower)

    # 3. Detect intent
    intent = _detect_intent(query_lower)

    # 4. Generate response based on intent
    response_text = ""
    if intent == "infrastructure":
        response_text = _respond_infrastructure(areas, traffic_df, query_lower)
    elif intent == "traffic":
        response_text = _respond_traffic(areas, traffic_df)
    elif intent == "route":
        response_text = _respond_route(areas, traffic_df)
    elif intent == "time":
        response_text = _respond_time(areas, traffic_df)
    elif intent == "safety":
        response_text = _respond_safety(areas, traffic_df)
    elif intent == "why":
        response_text = _respond_why(areas, traffic_df)
    elif intent == "prediction":
        response_text = _respond_prediction(areas, traffic_df)
    else:
        # If areas detected but no clear intent, give traffic status
        if areas:
            response_text = _respond_traffic(areas, traffic_df)
        else:
            # General Bangalore response
            response_text = _respond_general_bangalore(traffic_df)

    # 5. Generate dynamic suggestions
    suggestions = _generate_suggestions(intent, areas, user_role)

    return {
        "content": response_text,
        "suggestions": suggestions
    }

