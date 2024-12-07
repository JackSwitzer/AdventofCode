(* A simple OCaml test program *)

(* Define a simple function *)
let greet name =
  "Hello, " ^ name ^ "!"

(* Test some basic arithmetic *)
let sum = 5 + 3
let product = 4 * 6

(* Test the function and print results *)
let () =
  print_endline (greet "OCaml");
  print_endline ("Sum is: " ^ string_of_int sum);
  print_endline ("Product is: " ^ string_of_int product) 