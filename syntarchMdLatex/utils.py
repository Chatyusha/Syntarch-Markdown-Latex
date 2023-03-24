class Utils():
    @staticmethod
    def build_latex_environment(environment, contents, options = [],args=[]):
        _options = "".join([f"{{{option}}}" for option in options])
        _args = "".join([f"[{arg}]" for arg in args])
        return f"\\begin{{{environment}}}{_args}{_options}\n{contents}\n\\end{{{environment}}}"