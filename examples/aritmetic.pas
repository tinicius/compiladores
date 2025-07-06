program alu;

var
  a, b, c: integer;

begin
  a := 10;
  b := 3;

  c := a + b;      // ADD
  c := a - b;      // SUB
  c := a * b;      // MULT
  c := a div b;    // IDIV
  r := a / b;      // DIV
  c := a mod b;    // MOD

  write("Resultado: ", c);
end.
