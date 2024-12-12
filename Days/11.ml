(* Type definitions *)
type stone = int

(* Transform a single stone according to the rules *)
let transform_stone (stone: stone): stone array =
  if stone = 0 then [|1|]
  else
    let digits = String.length (string_of_int stone) in
    if digits mod 2 = 0 then
      let s = string_of_int stone in
      let mid = digits / 2 in
      let left = int_of_string (String.sub s 0 mid) in
      let right = int_of_string (String.sub s mid (digits - mid)) in
      [|left; right|]
    else
      [|stone * 2024|]

(* Process stones iteratively *)
let process_stones (input: string): unit =
  (* Parse initial stones into array *)
  let stones = 
    String.split_on_char ' ' input
    |> Array.of_list
    |> Array.map int_of_string
  in
  
  (* Iterate through steps *)
  let step = ref 0 in
  let current = ref stones in
  
  while !step <= 75 do
    (* Print results at checkpoints *)
    if !step = 25 then
      Printf.printf "Part 1: %d\n" (Array.length !current)
    else if !step = 75 then
      Printf.printf "Part 2: %d\n" (Array.length !current);
    
    if !step < 75 then begin
      (* Transform all stones *)
      let next = Array.concat (Array.to_list (Array.map transform_stone !current)) in
      current := next
    end;
    
    incr step
  done

let () =
  let ic = open_in "Data/11.txt" in
  let input = input_line ic in
  close_in ic;
  process_stones input
