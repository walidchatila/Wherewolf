package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;

public class GetPlayerResponse extends BasicResponse {

protected ArrayList <Players> players; 
	
	public GetPlayerResponse(String status, String errorMessage, ArrayList<Players> players){
		super(status, errorMessage);
		this.players = players; 
	}
	
	public ArrayList<Players> getPlayers(){
		return players;
	}
}
