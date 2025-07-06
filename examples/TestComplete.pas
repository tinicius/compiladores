program TestCompleto;
var i, j, soma: integer;
begin
soma := 0;
for i := 1 to 3 do
begin
  if i = 2 then continue;
  j := 1;
  while j <= 2 do
  begin
    soma := soma + i + j;
    writeln("i=", i, " j=", j, " soma=", soma);
    j := j + 1;
  end;
end;
writeln("Soma final: ", soma);
end.
