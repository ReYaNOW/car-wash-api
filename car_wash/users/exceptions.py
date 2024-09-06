class NoDefaultRoleError(ValueError):
    def __init__(self):
        super().__init__('Cannot find default role with name "client"')
