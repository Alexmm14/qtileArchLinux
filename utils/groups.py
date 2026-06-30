def groupTemplate(Match):
    APPS_CONFIG = {
        "Gemini": {
            "wm_class": "crx_aenkghcjmafhmiloejakejkpbhaipmjc",
             "group": "4"},
        "WhatsApp_Web": {
            "wm_class": "crx_hnpfjngllnobngcgfapefoaidbinmjnm",
             "group": "5"},
        "Spotify": {
            "wm_class": "crx_pjibgclleladliembfgfagdaldikeohf",
             "group": "5"},
    }


    # Creamos las listas de Match vacías para cada grupo del 1 al 5
    matches_by_group = {str(i): [] for i in range(1, 6)}

    for app in APPS_CONFIG.values():
        group_id = app["group"]
        if group_id in matches_by_group:
            matches_by_group[group_id].append(Match(wm_class=app["wm_class"]))

    groups =  [
        ("1", "●", matches_by_group["1"]),
        ("2", "●", matches_by_group["2"]), 
        ("3", "●", matches_by_group["3"]), 
        ("4", "●", matches_by_group["4"]), 
        ("5", "●", matches_by_group["5"]), 
    ]

    templateGroups = {
        "groups" : groups,
        "APPS_CONFIG" : APPS_CONFIG,
    }
    return templateGroups