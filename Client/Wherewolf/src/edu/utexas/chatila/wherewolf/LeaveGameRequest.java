package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import edu.utexas.chatila.wherewolf.BasicRequest.RequestType;

public class LeaveGameRequest extends BasicRequest {

protected final int gameID;
	
	public LeaveGameRequest(String username, String password, int gameID){
		super(username, password);
		this.gameID = gameID;
	}
	
	public int getGameID() { 
		return gameID;
	}
	
	@Override
	public String getURL()
	{
		return "/v1/game/" + Integer.toString(gameID); 
	}
	
	@Override
	public List<NameValuePair> getParameters(){
		return null;
	}
	
	@Override
	public RequestType getRequestType(){
		return RequestType.DELETE;
	}
	
	
	@Override
	public LeaveGameResponse execute(WherewolfNetworking net){
		
		
		      
		      try { 
		    	  
		    	  JSONObject response = net.sendRequest(this);
		          
			          
		          if (response.getString("status").equals("success"))
		          {
		        	  return new LeaveGameResponse("success",
				              "Successfully Left the game"
				              );
		          } else {
		              String errorMessage = response.getString("error");
		              return new LeaveGameResponse("failure", errorMessage);
		          }
		          
		      } catch (WherewolfNetworkException ex)
		      {
		          return new LeaveGameResponse("failure", "could not communicate with server.");
		      } catch (JSONException e) {
		          return new LeaveGameResponse("failure", "could not parse JSON.");
		      }
		      
		  }
}
