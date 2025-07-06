program EXS2;
var
n1, n2, media: real;
begin
writeln("Caro usuario, este programa recebera duas notas suas.");
writeln("Por favor, digite a primeira nota:");
readln(n1);
writeln("Agora digite a segunda nota:");
readln(n2);

media := (n1 + n2) / 2;
writeln("Sua media aritmetica e ", media, ".");

if (media >= 7) and (media <= 10) then
begin
  writeln("Voce foi aprovado!!!");
end
else
  if (media < 7) and (media >= 4) then
  begin
    writeln("Voce tera que fazer o exame.");
  end
  else
    if (media < 4) and (media >= 0) then
    begin
      writeln("Voce foi reprovado.");
    end
    else
    begin
      writeln("Media invalida.");
    end;
end.