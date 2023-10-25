class RemoteImage:
    """
    An image located on a remote computer that can be downloaded locally

    Attributes:
        remote_url  URL to the icon on a remote server
        local_url   Path to locally cached (and scaled) version of the icon
    """
    remote_url: str
    local_path: str | None = None

    def __init__(self, remote_url):
        self.remote_url = remote_url
