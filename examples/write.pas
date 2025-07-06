program Greeting;

var
  name: string;

begin

  writeln("A");
  writeln("A", name, "B");

  write("A");
  write("A", name, "B");

  readln(name);

end.