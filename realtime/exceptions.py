class FeatureMismatchError(Exception):
    def __init__(self, reason, **kwargs):
        self.reason = reason
        self.meta = kwargs
        super().__init__(reason)

    def details(self):
        return {"reason": self.reason, **self.meta}
