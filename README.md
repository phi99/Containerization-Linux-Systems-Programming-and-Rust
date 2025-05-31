***In Progress**

	 	---------------------------------------------------------------------------------------------------------
	     	  **  Implementing (Linux) Container from scratch with Rust **
	  	---------------------------------------------------------------------------------------------------------


```text
Container is basically build out of Linux features such as chroot, namespaces, and cgroups. Namespaces controls what a process can see.
There are several types of namespace in Linux, such as UTS (for hostname and domain names that the process is aware of), Process ID, Moount POints, Network, User and Group IDs, Inter-process communications (IPC), Control Groups(cgroups).
When linux system is started, it has a single namespace and a process is always in one namespace of each type. However, additional namespaes could be created and assign process into them.
Let's try to create a container in Rust by isolating a new process and to a UTS namespace.

-run() spawns a new process Command::new("/proc/self/exe").args(&child_args)
-this new process runs the same binary with args, enters chil()
-child() sets hostname, and spawns another process 
-Then Bash runs inside the namespace; parent child() process waits for it 
```
cargo run -- run /bin/bash


```text
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
```
