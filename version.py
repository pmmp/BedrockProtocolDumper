class Version():

    def __init__(self, major, minor, patch, revision, beta, protocol):

        self.major = major
        self.minor = minor
        self.patch = patch
        self.revision = revision
        self.beta = beta
        self.protocol = protocol



    def __str__(self):
        return 'Version: %d.%d.%d.%d\nProtocol: %d\nBeta: %d' % (self.major, self.minor, self.patch, self.revision, self.protocol, self.beta)

    def game_version(self):
        return ('v%d.%d.%d' % (self.major, self.minor, self.patch)) + (('.%d beta' % self.revision) if self.beta == 1 else '')

    def game_version_network(self):
        return ('%d.%d.%d' % (self.major, self.minor, self.patch)) + (('.%d' % self.revision) if self.beta == 1 else '')
