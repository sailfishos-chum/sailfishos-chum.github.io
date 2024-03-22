"""
Data classes for package metadata; this also parses metadata of a single package.
"""
import logging
from dataclasses import dataclass, field
import enum
from datetime import datetime, UTC
from enum import StrEnum
from types import NoneType
from typing import List, Dict, Self, Set, Optional

from markupsafe import Markup

from . import CONFIG
from .remote_image import RemoteImage

logger = logging.getLogger(__name__)

class PackageApplicationCategory(StrEnum):
    """
    Application categories, see https://specifications.freedesktop.org/menu-spec/latest/apa.html
    for main categories and https://specifications.freedesktop.org/menu-spec/latest/apas02.html
    for additional categories.
    """
    audiovideo = "AudioVideo"
    audio = "Audio"
    video = "Video"
    development = "Development"
    education = "Education"
    game = "Game"
    graphics = "Graphics"
    network = "Network"
    office = "Office"
    science = "Science"
    settings = "Settings"
    system = "System"
    utility = "Utility"
    other = "Other"
    building = "Building"
    debugger = "Debugger"
    ide = "IDE"
    guidesigner = "GUIDesigner"
    profiling = "Profiling"
    revisioncontrol = "RevisionControl"
    translation = "Translation"
    calendar = "Calendar"
    contactmanagement = "ContactManagement"
    database = "Database"
    dictionary = "Dictionary"
    chart = "Chart"
    email = "Email"
    finance = "Finance"
    flowchart = "FlowChart"
    pda = "PDA"
    projectmanagement = "ProjectManagement"
    presentation = "Presentation"
    spreadsheet = "Spreadsheet"
    wordprocessor = "WordProcessor"
    twodgraphics = "2DGraphics"
    vectorgraphics = "VectorGraphics"
    rastergraphics = "RasterGraphics"
    threedgraphics = "3DGraphics"
    scanning = "Scanning"
    ocr = "OCR"
    photography = "Photography"
    publishing = "Publishing"
    viewer = "Viewer"
    texttools = "TextTools"
    desktopsettings = "DesktopSettings"
    hardwaresettings = "HardwareSettings"
    printing = "Printing"
    packagemanager = "PackageManager"
    dialup = "Dialup"
    instantmessaging = "InstantMessaging"
    chat = "Chat"
    ircclient = "IRCClient"
    feed = "Feed"
    filetransfer = "FileTransfer"
    hamradio = "HamRadio"
    news = "News"
    p2p = "P2P"
    remoteaccess = "RemoteAccess"
    telephony = "Telephony"
    telephonytools = "TelephonyTools"
    videoconference = "VideoConference"
    webbrowser = "WebBrowser"
    webdevelopment = "WebDevelopment"
    midi = "Midi"
    mixer = "Mixer"
    sequencer = "Sequencer"
    tuner = "Tuner"
    tv = "TV"
    audiovideoediting = "AudioVideoEditing"
    player = "Player"
    recorder = "Recorder"
    discburning = "DiscBurning"
    actiongame = "ActionGame"
    adventuregame = "AdventureGame"
    arcadegame = "ArcadeGame"
    boardgame = "BoardGame"
    blocksgame = "BlocksGame"
    cardgame = "CardGame"
    kidsgame = "KidsGame"
    logicgame = "LogicGame"
    roleplaying = "RolePlaying"
    shooter = "Shooter"
    simulation = "Simulation"
    sportsgame = "SportsGame"
    strategygame = "StrategyGame"
    art = "Art"
    construction = "Construction"
    music = "Music"
    languages = "Languages"
    artificialintelligence = "ArtificialIntelligence"
    astronomy = "Astronomy"
    biology = "Biology"
    chemistry = "Chemistry"
    computerscience = "ComputerScience"
    datavisualization = "DataVisualization"
    economy = "Economy"
    electricity = "Electricity"
    geography = "Geography"
    geology = "Geology"
    geoscience = "Geoscience"
    history = "History"
    humanities = "Humanities"
    imageprocessing = "ImageProcessing"
    literature = "Literature"
    maps = "Maps"
    math = "Math"
    numericalanalysis = "NumericalAnalysis"
    medicalsoftware = "MedicalSoftware"
    physics = "Physics"
    robotics = "Robotics"
    spirituality = "Spirituality"
    sports = "Sports"
    parallelcomputing = "ParallelComputing"
    amusement = "Amusement"
    archiving = "Archiving"
    compression = "Compression"
    electronics = "Electronics"
    emulator = "Emulator"
    engineering = "Engineering"
    filetools = "FileTools"
    filemanager = "FileManager"
    terminalemulator = "TerminalEmulator"
    filesystem = "Filesystem"
    monitor = "Monitor"
    security = "Security"
    accessibility = "Accessibility"
    calculator = "Calculator"
    clock = "Clock"
    texteditor = "TextEditor"
    documentation = "Documentation"
    adult = "Adult"
    core = "Core"
    kde = "KDE"
    gnome = "GNOME"
    xfce = "XFCE"
    dde = "DDE"
    gtk = "GTK"
    qt = "Qt"
    motif = "Motif"
    java = "Java"
    consoleonly = "ConsoleOnly"


class PackageApplicationType(StrEnum):
    """
    Type of application a package provides

    Enums are based on https://www.freedesktop.org/software/appstream/docs/sect-AppStream-YAML.html#field-dep11-type
    """
    generic = enum.auto()
    console_application = "console-application"
    desktop_application = "desktop-application"
    addon = enum.auto()
    codec = enum.auto()
    inputmethod = enum.auto()
    firmware = enum.auto()


@dataclass
class PackageVersion:
    epoch: str
    ver: str
    rel: str

    def __init__(self, epoch, ver, rel):
        self.epoch = epoch
        self.ver = ver
        self.rel = rel

    def to_short_str(self) -> str:
        return self.ver.split('+', 2)[0]

    def to_full_str(self) -> str:
        return f"{self.ver}-{self.rel}"


@dataclass
class Package:
    """
    Metadata of an RPM package with associated metadata for SailfishOS:Chum
    """
    name: str
    summary: str | None = None
    description: str | Markup | None = None
    title: str | None = None
    icon: RemoteImage | None = None
    version: PackageVersion | None = None
    developer_name: str | None = None
    packager_name: str | None = None
    type: PackageApplicationType = PackageApplicationType.generic
    categories: Set[PackageApplicationCategory] = field(default_factory=lambda: {PackageApplicationCategory.other})
    screenshots: List[RemoteImage] = field(default_factory=list)
    links: Dict[str, str] = field(default_factory=dict)
    debuginfo_package: Self | None = None
    debugsource_package: Self | None = None
    url: str | None = None
    licence: str | None = None
    markdown_url: str | None = None
    repo_url: str | None = None
    packaging_repo_url: str | None = None
    debug_yaml: str | None = None
    debug_yaml_errors: List[Exception] = field(default_factory=list)
    updated: datetime | None = field(default_factory=lambda: datetime.fromtimestamp(0))

    repos: Set[str] = field(default_factory=set)
    archs: Set[str] = field(default_factory=set)
    download_size: Dict[str, int] = field(default_factory=dict)
    install_size: Dict[str, int] = field(default_factory=dict)
    download_url: Dict[str, str] = field(default_factory=dict)
    checksum_type: Dict[str, str] = field(default_factory=dict)
    checksum_value: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def from_node(dom_element, repo_arch: str):
        """
        Creates an instance of the class `Package` from a `<package>` XML node's `dom_element` as found in
        the `primary.xml` metadata file in RPM repositories.
        """

        def try_get_str(name) -> str | None:
            """Return content of XML tag with `name` or None"""
            try:
                return dom_element.getElementsByTagName(name)[0].firstChild.nodeValue
            except (IndexError, AttributeError):
                return None

        def try_get_attribute_tags(name, *args: str):
            result = (())
            try:
                el = dom_element.getElementsByTagName(name)[0]

                for attr in args:
                    result += (el.getAttribute(attr),)

                return result
            except IndexError:
                return tuple([None for _ in args])

        def try_get_version():
            """Parse version"""
            epoch, ver, rel = try_get_attribute_tags("version", "epoch", "ver", "rel")
            return PackageVersion(epoch, ver, rel)

        def name_to_title(name: str):
            name_parts: List[str] = name.split("-")
            if name_parts[0] == "harbour" or name_parts[0] == "openrepos":
                name_parts.pop(0)
            if name_parts[0].startswith("lib"):
                name_parts[0] = name_parts[0].removeprefix("lib")
                name_parts.append("(library)")
            if name_parts[-1] == "devel":
                name_parts[-1] = "(development files)"

            return " ".join(map(str.capitalize, name_parts))

        def parse_description(description: str, name: str):
            from yaml import safe_load as yaml_load
            from yaml.parser import ParserError
            from yaml.scanner import ScannerError

            import re
            # Based on
            # https://github.com/sailfishos-chum/sailfishos-chum-gui/blob/0b2882fad79673b762ca184cd242d02334f1d8d1/src/chumpackage.cpp#L152C1-L152C108
            # Metadata in YAML format which is put as last paragraph of the application description. Paragraphs are split by two newlines.
            paragraphs = [line for line in re.split(r"(?m)^\s*$", description) if line.strip()]
            if not paragraphs:
                return

            yaml_part = paragraphs.pop()
            p.debug_yaml = yaml_part
            try:
                yaml = yaml_load(yaml_part)
            except (ParserError, ScannerError):
                yaml = None
            # If the description is not valid YAML, it will be parsed as a `str` or generate a `ParserError`.
            # In the latter case, add the source back to the description.
            if type(yaml) in [str, NoneType]:
                paragraphs.append(yaml_part)
            else:
                # Note: Use `Dict.get()` to avoid `IndexError`s; we rather have None values.
                p.title = yaml.get("Title") or yaml.get("PackageName") or name_to_title(name)
                p.type = yaml.get("Type")

                icon_url = yaml.get("PackageIcon") or yaml.get("Icon")
                p.icon = RemoteImage(icon_url) if icon_url else None
                p.screenshots = list(map(lambda s: RemoteImage(s), yaml.get("Screenshots", [])))
                p.developer_name = yaml.get("DeveloperName")
                p.packager_name = yaml.get("PackagedBy")

                if "Custom" in yaml:
                    custom = yaml["Custom"]
                    if type(custom) is list:
                        custom_list = custom
                        custom = {}
                        # Handle cases where the Custom value is a list of key-value pairs instead of an object. :(
                        for list_item in custom_list:
                            custom |= {k: v for (k, v) in list_item.items()}

                    p.repo_url = custom.get("Repo")
                    p.packaging_repo_url = custom.get("PackagingRepo")
                    p.markdown_url = custom.get("DescriptionMD")

                try:
                    p.links = {key.lower(): val for key, val in (yaml.get("Links") or yaml.get("Url", {})).items()}
                except AttributeError as e:
                    p.debug_yaml_errors.append(e)

                try:
                    p.categories = set(map(PackageApplicationCategory, yaml["Categories"]))
                except (KeyError, ValueError) as e:
                    p.debug_yaml_errors.append(e)

            p.description = "\n\n".join(map(lambda s: s.replace('\n', ' '), paragraphs))

        arch = try_get_str("arch")

        p = Package(try_get_str("name"))
        p.repos.add(repo_arch)
        p.archs.add(arch)
        p.summary = try_get_str("summary")
        p.version = try_get_version()
        p.url = try_get_str("url")
        p.title = name_to_title(p.name)
        p.licence = try_get_str("rpm:license")
        p.updated = datetime.fromtimestamp(float(try_get_attribute_tags("time", "file")[0]), UTC)

        p.download_size[arch], p.install_size[arch] = try_get_attribute_tags("size", "package", "installed")
        p.download_url[arch] = try_get_attribute_tags("location", "href")[0]
        p.checksum_type[arch] = try_get_attribute_tags("checksum", "type")[0]
        p.checksum_value[arch] = try_get_str("checksum")

        try:
            parse_description(try_get_str("description"), p.name)
        except Exception as e:
            p.description = try_get_str("description")
            p.debug_yaml_errors.append(e)

        if p.name.startswith("lib") and PackageApplicationCategory.library not in p.categories:
            p.categories.add(PackageApplicationCategory.library)

        return p

    def merge_arch(self, other_pkg: Self):
        """
        Add the architecture-specific information from another package to this package.
        """
        for arch in other_pkg.archs:
            self.repos = self.repos.union(other_pkg.repos)
            self.download_size[arch] = other_pkg.download_size[arch]
            self.install_size[arch] = other_pkg.install_size[arch]
            self.download_url[arch] = other_pkg.download_url[arch]
            self.checksum_type[arch] = other_pkg.checksum_type[arch]
            self.checksum_value[arch] = other_pkg.checksum_value[arch]
            self.archs.add(arch)

    def is_app(self) -> bool:
        """
        Heuristic to detect whether this is a graphical application which a user is about to install.
        """
        return self.type == PackageApplicationType.desktop_application \
            or self.name.startswith("harbour-") \
            and not self.is_debug()

    def is_debug(self) -> bool:
        return self.name.endswith("-debuginfo") or self.name.endswith("-debugsource")

    def web_url(self):
        """
        Return URL for use in the web interface.
        """
        if self.is_app():
            return f"apps/{self.name}/"
        else:
            return f"pkgs/{self.name}/"

    def get_download_url(self, arch: str) -> Optional[str]:
        # noarch does not have a dedicated repository, use the first available arch I suppose
        # This may be an idea in the category "not smart"
        if arch == "noarch":
            repo = next(self.repos.__iter__())
        else:
            for repo in self.repos:
                repo_arch = repo.split("_")[1]
                if repo_arch == arch:
                    break
            else:
                logger.warning(f"No repo found for architecture {arch} (package: {self.name})")
                #assert False, f"No repo found for architecture {arch} (package: {self.name})"
                return None

        return f"{CONFIG.repo_url_prefix}{repo}/" + self.download_url[arch]


    def caused_requests(self):
        return type(self.markdown_url) == str

    def requested_urls(self):
        return [self.markdown_url]

    def to_search_dict(self):
        return {
            "name": self.name,
            "title": self.title,
            "url": self.web_url(),
            "icon": self.icon.remote_url if self.icon else None,
            "summary": self.summary,
            "description": self.description,
            "version": self.version.to_full_str(),
            "version_short": self.version.to_short_str(),
            "is_app": self.is_app(),
            "is_debug": self.is_debug()
        }
