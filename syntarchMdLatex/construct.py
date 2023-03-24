from syntarch.types import TokenTypes
from syntarch.types import TokenValues
from syntarch.token import Token

from syntarchMdLatex.utils import Utils

class Constructor(object):
    latex_text:str = ""
    def build_latex(self,tokens: list[Token]):
        contents_tree = []
        for token in tokens:
            if token.type == TokenTypes.TYPE_HEAD:
                contents_tree.append(self.build_head(token))
            elif token.type == TokenTypes.TYPE_PARAGRAPH:
                contents_tree.append(self.build_paragraph(token))
            elif token.type == TokenTypes.TYPE_QUOTE_BLOCK:
                contents_tree.append(self.build_quote_block(token))
            elif token.type == TokenTypes.TYPE_CODE_BLOCK:
                contents_tree.append(self.build_codeblock(token))
            elif token.type == TokenTypes.TYPE_TABLE:
                contents_tree.append(self.build_table(token))
            elif token.type == TokenTypes.TYPE_DOT_LIST:
                contents_tree.append(self.build_dot_list(token))
        self.latex_text = "\n\n".join(contents_tree)

    def build_emphasis(self,token : Token):
        return f"\\textbf{{{token.contents}}}"
    
    def build_italic(self,token : Token):
        return f"\\textit{{{token.contents}}}"
    
    def build_plaine(self,token : Token):
        return f"{token.contents}"
    
    def build_inline_math(self,token: Token):
        return f"${token.contents}$"
    
    def build_inline(self, token: Token):
        return f"\\colorbox[gray]{{0.9}}{{\\texttt{{{token.contents}}}}}"
    
    def build_context(self,context : list[Token]):
        latex_context = []
        for text_token in context:
            if text_token.type == TokenTypes.TYPE_EMPHASIS:
                latex_context.append(self.build_emphasis(text_token))
            elif text_token.type == TokenTypes.TYPE_ITALIC:
                latex_context.append(self.build_italic(text_token))
            elif text_token.type == TokenTypes.TYPE_PLAINE:
                latex_context.append(self.build_plaine(text_token))
            elif text_token.type == TokenTypes.TYPE_INLINE_MATH:
                latex_context.append(self.build_inline_math(text_token))
            elif text_token.type == TokenTypes.TYPE_INLINE:
                latex_context.append(self.build_inline(text_token))
        
        return "".join(latex_context)

    def build_paragraph(self,token:Token):
        return self.build_context(token.children)
    
    def build_head(self,token: Token):
        if token.level == 1:
            return f"\\part{{{token.contents}}}"
        elif token.level == 2:
            return f"\\section{{{token.contents}}}"
        elif token.level == 3:
            return f"\\subsection{{{token.contents}}}"
        elif token.level == 4:
            return f"\\subsubsection{{{token.contents}}}"
        elif token.level == 5:
            return f"\\paragraph{{{token.contents}}}"
        elif token.level == 6:
            return f"\\subparagraph{{{token.contents}}}"
    
    def build_codeblock(self,token: Token):
        latex_env = "lstlisting"
        return Utils.build_latex_environment(latex_env,token.contents)
        # return f"\\begin{{{latex_env}}}[]\n{token.contents}\n\\end{{{latex_env}}}"
    
    def build_quote_block(self,token: Token):
        latex_env = "quotation"
        _contents = self.build_context(token.children)
        return Utils.build_latex_environment(latex_env,_contents)
        # return f"\\begin{{{latex_env}}}\n{_contents}\n\\end{{{latex_env}}}"
    
    def build_table(self, token: Token):
        rows = []
        rows.append("\\hline")
        table_head = self.build_table_row(token.children.pop(0)) + "\\hline"
        rows.append(table_head)
        positions = self.build_table_positions(token.children.pop(0))
        for row in token.children:
            rows.append(self.build_table_row(row))
        _contents = "\n".join(rows)
        latex_env_table = "table"
        latex_env_tabular = "tabular"
        _tabular = Utils.build_latex_environment(environment=latex_env_tabular,contents=_contents, options=[positions])
        _table = Utils.build_latex_environment(latex_env_table,f"\\centering\n{_tabular}",args=["htb"])
        return _table
    
    def build_table_cell(self, token:Token):
        return self.build_context(token.children)

    def build_table_row(self,token: Token):
        return " & ".join([self.build_table_cell(cell) for cell in token.children]) + "\\\\ \\hline"
    
    def build_table_positions(self,token: Token):
        positoins = []
        for pos in token.children:
            if pos.contents == TokenValues.CONST_TABLE_POSITION_LEFT:
                positoins.append("l")
            elif pos.contents == TokenValues.CONST_POSITION_CENTER:
                positoins.append("c")
            elif pos.contents == TokenValues.CONST_POSITION_RIGHT:
                positoins.append("r")

        return "|" + "|".join(positoins) + "|"

    
    def build_dot_list(self,token: Token):
        _item = ""
        if token.children:
            _item = f"\\item {self.build_context(token.children)}"
        
        if token.items:
            _contents = [self.build_dot_list(i) for i in token.items]
            latex_env = "itemize"
            return "\n".join([_item,Utils.build_latex_environment(latex_env,"\n".join(_contents))])
        else:
            return _item