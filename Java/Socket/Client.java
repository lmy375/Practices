
import java.io.*;

import java.net.*;


public class Client {
	Socket conn;
	ObjectInputStream input;
	ObjectOutputStream output;
	InThread InputThread;
	OutThread OutputThread;
	
	
	public Client(String host, int portNumber){
		try{
		conn = new Socket(InetAddress.getByName(host),portNumber);
		System.out.println("Connecting...");
		input = new ObjectInputStream(conn.getInputStream());
		output = new ObjectOutputStream(conn.getOutputStream());
		output.flush();
		System.out.println("IOStream gotten");
		
		 
		 
		 InputThread= new InThread(input);
		 OutputThread= new OutThread(output);
		 while(!InputThread.runner.isAlive()||!OutputThread.runner.isAlive()){ 
		 
		input.close();
		output.close();
		conn.close();
		}
		
		}catch(Exception e){
			System.out.print(e.getMessage());					
		}
	}
	public static void main(String[] args){
		if(args.length<2) System.out.println("java Client [host][port]");
		else new Client(args[0],Integer.parseInt(args[1]));
	}
	
}

class InThread implements Runnable{
	Thread runner;
	ObjectInputStream input;
	public InThread(ObjectInputStream input){
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

class OutThread implements Runnable{
	Thread runner;
	ObjectOutputStream output;
	public OutThread(ObjectOutputStream output){
		this.output= output;
		runner = new Thread(this);
		runner.start();
	}
	public void run(){
		 BufferedReader bis = new BufferedReader (new InputStreamReader(System.in));
		 String in;
		 try{
			 while ((in= bis.readLine())!=null){
				 output.writeObject(in+"\n----by Client");			 
			 	System.out.println("----by you\n");
			 }
		 }catch(Exception e){
			 System.out.print(e.getMessage());
		 }
		 
	}
}
