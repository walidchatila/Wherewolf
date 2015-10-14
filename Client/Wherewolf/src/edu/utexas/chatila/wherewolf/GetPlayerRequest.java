package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import edu.utexas.chatila.wherewolf.BasicRequest.RequestType;


public class GetPlayerRequest extends BasicRequest {
	
	public final int gameID;

	public GetPlayerRequest(String username, String password, int gameID){
		super(username, password);
		this.gameID = gameID; 
	
	}
	
	@Override
	public String getURL(){
		
		
		return "/v1/game/" + Integer.toString(gameID); 
	}
	
	@Override
	public List<NameValuePair> getParameters(){
		return null;
	}

	@Override
	public RequestType getRequestType(){
		return RequestType.GET;
	}
	
	@Override
	public GetPlayerResponse execute(WherewolfNetworking net){
		
		ArrayList<Players> players = new ArrayList<Players>(); 
		
		try {
			
			JSONObject jObject = net.sendRequest(this);
			
			JSONArray jArray = jObject.getJSONArray("players");
			for (int i = 0; i < jArray.length(); i++){
				try{
					JSONObject oneObject = jArray.getJSONObject(i); 
					String username = oneObject.getString("username"); 
					
					players.add(new Players(username, "male")); 
					
				} catch (JSONException e){
					//oops
				}
			}
		} catch (JSONException e){}
		catch (WherewolfNetworkException ex)
		{ 
			return new GetPlayerResponse("failure", "could not communicated with server", players);
		}
		
		return new GetPlayerResponse("success","got games", players);
	}
}

