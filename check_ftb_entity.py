import sys
import requests

def check(entity_id: str) -> dict:
    """Checks the status of a California Franchise Tax Board (FTB) entity.

    Args:
        entity_id: The entity ID.

    Returns:
        A dictionary containing the entity information, or `None` if the entity cannot be found.
    """

    data = {
        "_Fingerprint": "",
        "EntityId": entity_id,
        "SearchMethodType": "1",
        "EntityName": "",
        "__RequestVerificationToken": "",
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    }

    with requests.Session() as session:
        response = session.get("https://webapp.ftb.ca.gov/eletter/Home/Index", headers=headers)
        response = session.post("https://webapp.ftb.ca.gov/eletter", headers=headers, data=data)
        response = session.get(
            "https://webapp.ftb.ca.gov/eletter/Home/Summary?entityID=" + entity_id,
            headers=headers,
        )

        info = {}
        info["entityName"] = response.text.split("Entity Name:")[-1].split("</b>", 1)[0].split(
            "<b>"
        )[-1]
        info["address"] = response.text.split("Address:")[-1].split("</b>", 1)[0].split(
            "<b>"
        )[-1]
        info["entityStatus"] = response.text.split("Entity Status:")[-1].split("</b>", 1)[
            0
        ].split("<b>")[-1]
        info["exemptStatus"] = response.text.split("Exempt Status:")[-1].split("</b>", 1)[
            0
        ].split("<b>")[-1]

        if info["entityStatus"]:
            return info
        else:
            return None


if __name__ == "__main__":
    entity_id = sys.argv[1]

    entity_info = check(entity_id)

    if entity_info is not None:
        print("Entity Name:", entity_info["entityName"])
        print("Address:", entity_info["address"])
        print("Entity Status:", entity_info["entityStatus"])
        print("Exempt Status:", entity_info["exemptStatus"])
    else:
        print("Entity Not Found !!")
