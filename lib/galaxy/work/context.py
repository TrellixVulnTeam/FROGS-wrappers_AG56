from galaxy.managers.context import (
    ProvidesHistoryContext,
)


class WorkRequestContext(ProvidesHistoryContext):
    """ Stripped down implementation of Galaxy web transaction god object for
    work request handling outside of web threads - uses mix-ins shared with
    GalaxyWebTransaction to provide app, user, and history context convenience
    methods - but nothing related to HTTP handling, mako views, etc....

    Things that only need app shouldn't be consuming trans - but there is a
    need for actions potentially tied to users and histories and  hopefully
    this can define that stripped down interface providing access to user and
    history information - but not dealing with web request and response
    objects.
    """

    def __init__(self, app, user=None, history=None, workflow_building_mode=False):
        self._app = app
        self.__user = user
        self.__user_current_roles = None
        self.__history = history
        self.workflow_building_mode = workflow_building_mode

    @property
    def app(self):
        return self._app

    def get_history(self, create=False):
        return self.__history

    @property
    def history(self):
        return self.get_history()

    def get_user(self):
        """Return the current user if logged in or None."""
        return self.__user

    def get_current_user_roles(self):
        if self.__user_current_roles is None:
            self.__user_current_roles = super().get_current_user_roles()
        return self.__user_current_roles

    def set_user(self, user):
        """Set the current user."""
        raise NotImplementedError("Cannot change users from a work request context.")

    user = property(get_user, set_user)


class SessionRequestContext(WorkRequestContext):
    """Like WorkRequestContext, but provides access to galaxy session and session."""
    def __init__(self, **kwargs):
        self.galaxy_session = kwargs.pop('galaxy_session', None)
        super().__init__(**kwargs)

    def get_galaxy_session(self):
        return self.galaxy_session
