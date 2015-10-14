package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;
import java.util.List;

public class GetGameResponse extends BasicResponse {

	protected ArrayList <Games> games; 
	
	public GetGameResponse(String status, String errorMessage, ArrayList<Games> games){
		super(status, errorMessage);
		this.games = games; 
	}
	
	public ArrayList<Games> getGames(){
		return games;
	}
}
