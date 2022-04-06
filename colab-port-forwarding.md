1. [GPU node] Install Jupyterlab, notebook, and Jupyter HTTP over WebSocket
	
	`pip3 install jupyterlab notebook jupyter_http_over_ws`

	Note: Add `~/.local/bin` to your PATH

2. [GPU node] Install and enable the jupyter_http_over_ws jupyter extension

	`jupyter serverextension enable --py jupyter_http_over_ws`

3. [GPU node] Start Jupyter server and authenticate

	`nohup jupyter notebook \
--no-browser \
--NotebookApp.answer_yes=True \
--log-level=DEBUG \
--NotebookApp.allow_origin='https://colab.research.google.com' \
--port=8888 \
--ServerApp.port_retries=0 \
--ip=0.0.0.0 &
  	`

  	* This will print backend URL for authentication. Options are explained below:
  	* Don't open browser
  	* Answer yes to all questions
  	* Set log level to Debug for debugging
  	* Allow connection from Google Colab
  	* Start the server on port 8888
  	* Don't retry for other ports
  	* Allow connections from any IP (use "ip" and not NotebookApp.ip or ServerApp.ip)

4. [Local machine] SSH port forward a specific port to port 8888 on GPU node
	
	`ssh <username>@<remote_IP> -N -f -L <local_port>:<remote_IP>:<remote_port>
	 # ssh pratik@133.11.34.101 -N -v -L 8888:133.11.34.101:8888	(local <-> Gateway server)
	 # ssh pratik@133.11.34.101 -N -v -L 8888:133.11.34.102:8888	(local <-> Gateway server <-> GPU Node)
	`

	* The options are explained below:
	* -N: Do not execute a remote command.  This is useful for just forwarding ports
	* -f: Requests ssh to go to background just before command execution.  This is useful if ssh is going to
        ask for passwords or passphrases, but the user wants it in the background (For running experiments)
    * -L: Specifies that the given port on the local (client) host is to be forwarded to the given host and
        port on the remote side
    * -v: For verbose output (For experiments and debugging)


4. Open http://localhost:8888

5. Do not forget to stop the port forwarding on your local machine and jupyter notebook app on the GPU node


## References
https://research.google.com/colaboratory/local-runtimes.html
https://www.concordia.ca/ginacody/aits/support/faq/ssh-tunnel.html
https://thedatafrog.com/en/articles/remote-jupyter-notebooks/
https://explainshell.com/explain?cmd=ssh+-L+-N+-f+-l
