class RemoteImage:
    """
    An image located on a remote computer that can be downloaded locally.

    Attributes:
        remote_url  URL for an icon on a remote server
        local_url   Local URL (path) to cached (and scaled) version of this icon
    """
    remote_url: str
    local_path: str | None = None

    def __init__(self, remote_url):
        self.remote_url = remote_url
