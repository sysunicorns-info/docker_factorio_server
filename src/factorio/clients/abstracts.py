"""
Provides the abstract client class
"""

from abc import abstractmethod

from httpx import AsyncClient, AsyncHTTPTransport

from factorio.configs import FactorioCliSettings


class AbstractClient:
    """
    Abstract client class
    """

    _transport: AsyncHTTPTransport
    _settings: FactorioCliSettings

    _timeout: int | None = None
    _retries: int | None = None
    _base_url: str | None = None

    def _setup_transport(self) -> AsyncHTTPTransport:
        """
        Setup the transport
        """
        return AsyncHTTPTransport(retries=self._settings.server_mod_client_retries)

    @abstractmethod
    def _setup(self) -> None:
        """
        Setup the base url

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError

    def _validate_setup(self) -> None:
        """
        Validate the setup

        Returns:
            None

        Raises:
            ValueError: If the base url is not set
        """
        if self._base_url is None:
            raise ValueError("The base url is not set")
        if self._retries is None:
            raise ValueError("The retries is not set")
        if self._timeout is None:
            raise ValueError("The timeout is not set")

    def __init__(self, factorio_client_settings: FactorioCliSettings) -> None:
        """
        Initialize the client with the settings

        Args:
            factorio_client_settings (FactorioCliSettings): The settings

        Raises:
            ValueError: If base_url, retries, ... is not set
        """

        # Get the settings
        self._settings = factorio_client_settings

        # Provide capability to override settings like base_url and retries
        # from child classes
        self._setup()

        # Validate the setup to make sure we have the base url, retries, ...
        self._validate_setup()

        # Setup the transport
        self._transport = self._setup_transport()

    def _get_client(self) -> AsyncClient:
        """
        Get the client from the transport
        Returns:
            AsyncClient: The client
        """
        return AsyncClient(
            transport=self._transport,
            base_url=self._base_url,
            timeout=self._timeout,
        )
