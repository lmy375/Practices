
import java.io.*;

import java.net.*;

public class Server {
	ServerSocket server;
	Socket conn;
	ObjectOutputStream output;
	ObjectInputStream input;
	InThread2 InputThread;
	OutThread2 OutputThread;
	public Server(int portNumber ,int queueLength){
		 try{
			 server = new ServerSocket(portNumber,queueLength);
			 System.out.print("Waiting for Client...\n");
			 conn = server.accept();
			 System.out.println("Client gotten");
			 System.out.println("Setting IOStream...");
			 output= new ObjectOutputStream(conn.getOutputStream());
			 output.flush();
			 input = new ObjectInputStream(conn.getInputStream());
			 System.out.println("IOStream setted.");
			 
			 InputThread= new InThread2(input);
			 OutputThread= new OutThread2(output);
			 
			while(!InputThread.runner.isAlive()||!OutputThread.runner.isAlive()){ 
			 
			input.close();
			output.close();
			conn.close();
			}
			
			
			 
		 }catch (IOException ioe){
			 System.out.print(ioe.getMessage());
		 }
		 
		 
	}
	public static void main(String[] args){
		if(args.length<2) System.out.println("java Server [portNumber][queueLength]");
		else new Server(Integer.parseInt(args[0]), Integer.parseInt(args[1]));
	}
	
}

class InThread2 implements Runnable{
	Thread runner;
	ObjectInputStream input;
	public InThread2(ObjectInputStream input){
		this.input= input;
		runner  = new Thread(this);
		runner.start();
	}
	public void run(){
		
			 String in;
			 try{
			 while ((in=input.readObject().toString() )!=null)
				 System.out.println(in);
			 }
			 catch(Exception e){
				 System.out.print(e.getMessage());
			 }
	}
}

class OutThread2 implements Runnable{
	Thread runner;
	ObjectOutputStream output;
	public OutThread2(ObjectOutputStream output){
		this.output= output;
		runner = new Thread(this);
		runner.start();
	}
	public void run(){
		 BufferedReader bis = new BufferedReader (new InputStreamReader(System.in));
		 String in;
		 try{
			 while ((in= bis.readLine())!=null){
				 output.writeObject(in+"\n----by Server\n");
				 System.out.println("----by you\n");
			 }
		 }catch(Exception e){
			 System.out.print(e.getMessage());
		 }
		 
	}
}

