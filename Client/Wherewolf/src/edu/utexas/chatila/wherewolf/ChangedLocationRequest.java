package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

public class ChangedLocationRequest extends BasicRequest {
	public final int gameID;
	public ChangedLocationRequest(String username, String password, int gameID) {
		super(username, password);
		this.gameID = gameID;
		
		}
	@Override
	public String getURL() {
		return "v1/game/" + Integer.toString(gameID);
	}
	@Override
	public List<NameValuePair> getParameters() {
		List<NameValuePair> urlParameters = new ArrayList<NameValuePair>();
		urlParameters.add(new BasicNameValuePair("gameID", Integer.toString(gameID)));		
		return urlParameters;
	}
	@Override
	public RequestType getRequestType() {
		return RequestType.PUT;
	}
	@Override
	public ChangedLocationResponse execute(WherewolfNetworking net) {
	      try {
	          JSONObject response = net.sendRequest(this);
	          
	          if (response.getString("status").equals("success"))
	          {
	              // String lat = response.getString("lat");
	        	// String lng = response.getString("lng");
	              return new ChangedLocationResponse("success", "changed location",gameID);
	          } else {
	              
	              String errorMessage = response.getString("error");
	              return new ChangedLocationResponse("failure", errorMessage, gameID);
	          }
	      } catch (JSONException e) {
	          return new ChangedLocationResponse("failure", "not able to change location", gameID);
	      } catch (WherewolfNetworkException ex)
	      {
	          return new ChangedLocationResponse("failure", "could not communicate with the server", gameID);
	      }
	}
}