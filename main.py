import os
import json
import requests
from enum import Enum
from typing import Generator
from dotenv import load_dotenv
from urllib.parse import urljoin
from dataclasses import dataclass, field


class Constants(Enum):
    API = "https://ossindex.sonatype.org/api/v3/"
    COMPONENT_REPORT = "component-report"
    MAX_PACKAGES = 128


@dataclass
class Package:
    name: str
    version: str
    coordinates: str = field(init=False)

    def __post_init__(self):
        self.version = (
            self.version.split("+")[0] if "+" in self.version else self.version
        )
        self.coordinates = f"pkg:pypi/{self.name}@{self.version}"


def call_api(
    pkgs: list[Package],
    username: str | None = None,
    token: str | None = None,
) -> Generator:
    url = urljoin(Constants.API.value, Constants.COMPONENT_REPORT.value)
    auth = (username, token) if username and token else None
    index = {pkg.coordinates.lower(): pkg for pkg in pkgs}
    for i in range(0, len(pkgs), Constants.MAX_PACKAGES.value):
        coordinates = [
            p.coordinates for p in pkgs[i : i + Constants.MAX_PACKAGES.value]
        ]
        res = requests.post(
            url, auth=auth, json={"coordinates": coordinates}, timeout=20
        )

        if res.status_code == 200:
            for entry in res.json():
                pkg = index.get(entry["coordinates"].lower(), Package("unknown", "0"))
                yield (pkg, entry)
        elif res.status_code == 401:
            raise Exception("Invalid Credentials.")
        elif res.status_code == 429:
            raise Exception("Too many requests.")
        else:
            raise Exception(f"Unknown status code {res.status_code}.")


def get_vulnerabilities(env_packages: list[dict[str, str]]):
    pkgs = [Package(p["name"], p["version"]) for p in env_packages]
    token = os.getenv("OSSINDEX_API_TOKEN", None)
    user = os.getenv("OSSINDEX_API_USERNAME", None)
    vulns = []
    refs = []
    try:
        for pkg, entry in call_api(pkgs, username=user, token=token):
            vuln = entry.get("vulnerabilities") if pkg.name != "unknown" else None
            ref = entry.get("reference") if pkg.name != "unknown" else None
            vulns.append(vuln)
            refs.append(ref)
    except Exception as e:
        raise e
    return vulns, refs


if __name__ == "__main__":
    load_dotenv()
    # load packages
    input_path = "sample_packages.json"
    with open(input_path) as f:
        pakcages = json.load(f)

    vulns, refs = get_vulnerabilities(pakcages)
    for p, vuln, ref in zip(pakcages, vulns, refs):
        p["vulnerabilities"] = vuln
        p["reference"] = ref

    output_path = "sample_packages_info.json"
    with open(output_path, "w+") as f:
        json.dump(pakcages, f, indent=4)
