package edu.utexas.chatila.wherewolf;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

import edu.utexas.chatila.wherewolf.BasicRequest.RequestType;

public class CreateUserRequest extends BasicRequest{

	  private final String firstName;
	  private final String lastName;
	  
	  public CreateUserRequest(String username, String password,
	          String firstName, String lastName) {
	      
	      super(username, password);
	      
	      this.firstName = firstName;
	      this.lastName = lastName;
	  }

	  public String getfirstName() {
	      return firstName;
	  }
	  
	  public String lastName() {
	      return lastName;
	  }


	  @Override
	  public String getURL() {
	      return "/v1/register";
	  }
	  
	  @Override
	  public RequestType getRequestType()
	  {
	      return RequestType.POST;
	  }

	  @Override
	  public List<NameValuePair> getParameters() {
	      List<NameValuePair> urlParameters = new ArrayList<NameValuePair>();
	      urlParameters.add(new BasicNameValuePair("firstname", firstName));
	      urlParameters.add(new BasicNameValuePair("lastname", lastName));
	      urlParameters.add(new BasicNameValuePair("username", username));
	      urlParameters.add(new BasicNameValuePair("password", password));
	      return urlParameters;
	  }
	  

	  @Override
	  public CreateUserResponse execute(WherewolfNetworking net) {
	      
	      try {
	          JSONObject jObject = net.sendRequest(this);
	          
	          String status = jObject.getString("status");
	          
	          if (status.equals("success"))
	          {
	              return new CreateUserResponse("success", "created user");
	          } else {
	              String errorMessage = jObject.getString("error");
	              return new CreateUserResponse("failure", errorMessage);
	          }
	          
	      } catch (WherewolfNetworkException ex)
	      {
	          return new CreateUserResponse("failure", "could not communicate with server.");
	      } catch (JSONException e) {
	          return new CreateUserResponse("failure", "could not parse JSON.");
	      }
	      
	  }
	  
	}