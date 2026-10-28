# ============================================================
# LUMINA AI
# Personalized Preventive Recommendations
# ============================================================


def generate_recommendations(
    uv_index,
    pm25,
    temperature,
    humidity,
    outdoor_hours,
    stress_score
):

    recommendations = []

    # --------------------------------------------------------
    # UV
    # --------------------------------------------------------

    if uv_index >= 8:

        recommendations.append({
            "title": "High UV exposure",
            "text": "Prioritize daily photoprotection and reduce unnecessary direct sun exposure."
        })

    elif uv_index >= 3:

        recommendations.append({
            "title": "Moderate UV exposure",
            "text": "Maintain consistent daily photoprotection, especially during outdoor activities."
        })

    # --------------------------------------------------------
    # PM2.5
    # --------------------------------------------------------

    if pm25 >= 100:

        recommendations.append({
            "title": "High air pollution",
            "text": "Limit prolonged outdoor exposure when possible and keep your cleansing routine gentle."
        })

    elif pm25 >= 35:

        recommendations.append({
            "title": "Elevated air pollution",
            "text": "Pay attention to gentle cleansing and barrier-supportive skincare after outdoor exposure."
        })

    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    if temperature >= 35:

        recommendations.append({
            "title": "High temperature",
            "text": "Stay hydrated and consider a lightweight skincare routine during hot conditions."
        })

    elif temperature <= 18:

        recommendations.append({
            "title": "Cool conditions",
            "text": "Support skin comfort with adequate hydration and a gentle routine."
        })

    # --------------------------------------------------------
    # HUMIDITY
    # --------------------------------------------------------

    if humidity >= 80:

        recommendations.append({
            "title": "High humidity",
            "text": "Keep the routine lightweight and avoid unnecessarily heavy layers."
        })

    elif humidity <= 35:

        recommendations.append({
            "title": "Low humidity",
            "text": "Give extra attention to hydration and maintaining the skin barrier."
        })

    # --------------------------------------------------------
    # OUTDOOR EXPOSURE
    # --------------------------------------------------------

    if outdoor_hours >= 5:

        recommendations.append({
            "title": "Long outdoor exposure",
            "text": "Consider stronger preventive protection when spending extended time outdoors."
        })

    elif outdoor_hours >= 2:

        recommendations.append({
            "title": "Regular outdoor exposure",
            "text": "Keep your preventive routine consistent on days with extended outdoor activity."
        })

    # --------------------------------------------------------
    # GENERAL RESULT
    # --------------------------------------------------------

    if stress_score >= 80:

        recommendations.insert(
            0,
            {
                "title": "Higher environmental stress",
                "text": "Today's conditions suggest using a consistent preventive skincare routine."
            }
        )

    elif stress_score >= 60:

        recommendations.insert(
            0,
            {
                "title": "Elevated environmental stress",
                "text": "Your environment may benefit from a more consistent protective routine today."
            }
        )

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    if not recommendations:

        recommendations.append({
            "title": "Balanced conditions",
            "text": "Your current environmental conditions appear relatively balanced. Maintain your regular skincare routine."
        })

    # Only show the first 4 recommendations
    return recommendations[:4]