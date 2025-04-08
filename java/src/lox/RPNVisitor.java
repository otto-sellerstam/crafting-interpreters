package lox;

class RPNVisitor implements Expr.Visitor<String> {
    String print(Expr expr) {
        return expr.accept(this);
    }

    @Override
    public String visitBinaryExpr(Expr.Binary expr) {
        return RPN(expr.operator.lexeme, expr.left, expr.right);
    }

    @Override
    public String visitGroupingExpr(Expr.Grouping expr) {
        return expr.expression.accept(this);
    }

    @Override
    public String visitLiteralExpr(Expr.Literal expr) {
        if (expr.value == null) return "nil";
        return expr.value.toString();
    }

    @Override
    public String visitUnaryExpr(Expr.Unary expr) {
        return "";
    }

    private String RPN(String symbol, Expr left, Expr right) {
        StringBuilder builder = new StringBuilder();

        builder.append(left.accept(this));
        builder.append(" ");
        builder.append(right.accept(this));
        builder.append(" ");
        builder.append(symbol);

        return builder.toString();
    }

    public static void main(String[] args) {
        Expr expression = new Expr.Binary(
            new Expr.Binary(
                new Expr.Literal(2),
                new Token(TokenType.PLUS, "+", null, 1),
                new Expr.Literal(3)
            ),
            new Token(TokenType.STAR, "*", null, 1),
            new Expr.Grouping(
                new Expr.Binary(
                    new Expr.Literal(5),
                    new Token(TokenType.MINUS, "-", null, 1),
                    new Expr.Unary(new Token(TokenType.MINUS, "-", null, 1), new Expr.Literal(1))
                )
            )
        );
        System.out.println(new RPNVisitor().print(expression));
    }
}