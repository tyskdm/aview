
class Debug:

    def __init__(self, logger) -> None:
        self._logger = logger
        self._indent = 0
        self._putsbuff = ''


    def indent(self, n=1) -> None:
        self._indent += n


    def undent(self, n=1) -> None:
        self._indent -= n


    def print(self, message, indent=0) -> None:
        space = ''
        for _ in range(self._indent + indent):
            space += '  '

        message = self._putsbuff + message
        self._putsbuff = ''

        lines = message.split('\n')
        for line in lines:
            self._logger.debug(space + line)


    def puts(self, message) -> None:
        self._putsbuff += message

        lines = self._putsbuff.split('\n')
        if len(lines) > 1:
            self._putsbuff = ''

            for line in lines[:-1]:
                self.print(line)

            self._putsbuff = lines[-1]
