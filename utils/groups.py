def groupTemplate(Match):
    APPS_CONFIG = {
        "Visual_Studio_Code": {
            "wm_class": "code-oss",
             "group": "1"},
        "Android_Studio": {
            "wm_class": "jetbrains-studio", 
            "group": "1"},
        "Microsoft_TeamsCoopeuch": {
            "wm_class": "crx_ompifgpmddkgmclendfeacglnodjjndh",
             "group": "2"},
        "Microsoft_TeamsWolf": {
            "wm_class": "crx_ompifgpmddkgmclendfeacglnodjjndh",
             "group": "2"},
        "Discord": {
            "wm_class": "discord",
             "group": "3"},
        "Oracle_VirtualBox": {
            "wm_class": "VirtualBox Manager",
             "group": "4"},
        "Oracle_VirtualBox": {
            "wm_class": "VirtualBox Machine",
            "group": "4"},
        "Chrome_Remote_Desktop": {
            "wm_class": "crx_cmkncekebbebpfilplodngbpllndjkfo",
             "group": "4"},
        "obs": {
            "wm_class": "obs",
             "group": "4"},
        "Gemini": {
            "wm_class": "crx_aenkghcjmafhmiloejakejkpbhaipmjc",
             "group": "4"},
        "GitHub": {
            "wm_class": "crx_mjoklplbddabcmpepnokjaffbmgbkkgg",
             "group": "4"},
        "Grafana": {
            "wm_class": "crx_anfppppmoajijngmjhcciakbdeehpape",
             "group": "4"},
        "LibreOffice_Base": {
            "wm_class": "libreoffice-base",
            "group": "4"},
        "LibreOffice_Calc": {
            "wm_class": "libreoffice-calc",
            "group": "4"},
        "LibreOffice_Draw": {
            "wm_class": "libreoffice-draw",
            "group": "4"},
        "LibreOffice_Impress": {
            "wm_class": "libreoffice-impress",
            "group": "4"},
        "LibreOffice_Math": {
            "wm_class": "libreoffice-math",
            "group": "4"},
        "LibreOffice": {
            "wm_class": "libreoffice-startcenter",
            "group": "4"},
        "LibreOffice_Writer": {
            "wm_class": "libreoffice-writer",
            "group": "4"},
        "YouTube_Music": {
            "wm_class": "crx_cinhimbnkkaeohfgghhklpknlkffjgod",
             "group": "5"},
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