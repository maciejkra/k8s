
# Task – Docker Volume

## Goal

Learn how to use Docker volumes:
- Mount a local directory from your host (bind mount)
- Use named Docker volumes
- Understand read-only (`:ro`) and read-write (`:rw`) mount options

---

## Part A: Bind Mount with Local Directory

1. Build the image from the provided `01_volume_ls` directory:

   ```bash
   docker build -t my-nginx 01_volume_ls
   ```

2. Run the container with the current directory mounted into `/data`:


     ```
     docker run --rm -it -v "${PWD}:/data" my-nginx
     ```

3. Create a file inside the mounted directory:

   - On Linux/macOS:

     ```bash
     touch ./something.txt
     ```

   - On Windows (since `touch` may not be available):

     ```powershell
     echo Hello > something.txt
     ```

4. Check from inside the container that the file is visible in `/data`.

---

## Part B: Named Volume with Read-Only and Read-Write

1. Create a named Docker volume:

   ```bash
   docker volume create my-volume
   ```

2. Run two containers using the same volume:

   - **Read-only container**:

     ```bash
     docker run -d --name ro-container -v my-volume:/data:ro my-nginx
     ```

   - **Read-write container**:

     ```bash
     docker run -d --name rw-container -v my-volume:/data my-nginx
     ```

3. From the `rw-container`, create a file:

   ```bash
   docker exec rw-container sh -c "echo 'Hello from RW' > /data/hello.txt"
   ```

4. From the `ro-container`, verify the file exists:

   ```bash
   docker exec ro-container ls /data
   docker exec ro-container cat /data/hello.txt
   ```

5. Try creating a file in the `ro-container` (should fail):

   ```bash
   docker exec ro-container sh -c "echo 'nope' > /data/fail.txt"
   ```

   You should get a **permission denied** error, proving the volume is mounted read-only.

---

## Summary

- Bind mounts link your local filesystem into the container — good for development.
- Named volumes are managed by Docker and survive container deletion.
- `:ro` protects data from being modified by the container.
