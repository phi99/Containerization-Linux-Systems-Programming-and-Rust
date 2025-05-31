//in progress


use std::env;
use std::process::{Command, Stdio};
use nix::sched::{unshare, CloneFlags};
use nix::unistd::sethostname;

fn main() {
  let args: Vec<String> = env::args().collect();
  if args.len() < 2 {
    panic!("usage: run <cmd> <args>...");
  }

  match args[1].as_str() {
    "run" => run(&args),
    "child" => child(&args),
    _ => panic!("expected 'run' or 'child'"),
  }
}

fn run(args: &[String]) {
  println!("Running {:?}", &args[2..]);

  let mut child_args = vec!["child".to_string()];
  child_args.extend_from_slice(&args[2..]);

  let mut cmd = Command::new("/proc/self/exe")
  .args(&child_args)
  .stdin(Stdio::inherit())
  .stdout(Stdio::inherit())
  .stderr(Stdio::inherit())
  .spawn()
  .expect("Failed to create child process");

  let status=cmd.wait().expect("failed to wait for child");
  if !status.success() {
    panic!("Child exited with error");
  }
}

fn child(args: &[String]) {
  println!(
