CDP_OUTPUT_WITH_MERGED_LAST_COLUMNS = """
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone
Device ID    Local Intrfce   Holdtme    Capability   Platform Port ID
Router       Fas 0/1          141            R       ISR4300- Gig 0/0/1
Switch       Fas 0/3          141            R       ISR4300- Gig 0/0/1
"""

CDP_OUTPUT_REGULAR_CASE = """
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone
Device ID    Local Intrfce   Holdtme    Capability   Platform    Port ID
Router       Fas 0/1          141            R       ISR4300     Gig 0/0/1
Switch       Fas 0/3          141            R       ISR4300     Gig 0/0/1
"""

CDP_OUTPUT_ROUTER = """
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone
Device ID    Local Intrfce   Holdtme    Capability   Platform Port ID
Switch       Fas 0/3          141            R       ISR4300- Gig 0/0/1
"""

CDP_OUTPUT_SWITCH = """
Capability Codes: R - Router, T - Trans Bridge, B - Source Route Bridge
                  S - Switch, H - Host, I - IGMP, r - Repeater, P - Phone
Device ID    Local Intrfce   Holdtme    Capability   Platform Port ID
Router       Fas 0/1          141            R       ISR4300- Gig 0/0/1
"""

ROUTER_CONFIG = "mocked config"
SWITCH_CONFIG = "mocked config"
ROUTER_HOSTNAME = "Router"
SWITCH_HOSTNAME = "Switch"
ROUTER_VERSION = "Mocked version of Router"
SWITCH_VERSION = "Mocked version of Switch"
