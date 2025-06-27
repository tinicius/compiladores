program alu;

var
  a, b, c: integer;
  r: real;
  s: string;
  logic: boolean;

begin
  a := 10;
  b := 3;

  c := a + b;      // ADD
  c := a - b;      // SUB
  c := a * b;      // MULT
  c := a div b;    // IDIV
  r := a / b;      // DIV
  c := a mod b;    // MOD

  logic := a = b;      // EQ
  logic := a <> b;     // NEQ
  logic := a < b;      // LESS
  logic := a <= b;     // LEQ
  logic := a > b;      // GRET
  logic := a >= b;     // GEQ

  logic := (a > 0) and (b > 0); // AND
  logic := (a > 0) or (b < 0);  // OR
  logic := not (a = b);         // NOT
end.
