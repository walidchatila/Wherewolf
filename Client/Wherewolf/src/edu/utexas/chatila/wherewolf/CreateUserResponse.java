package edu.utexas.chatila.wherewolf;

public class CreateUserResponse extends BasicResponse {

	  private int userID = -1;

	  public CreateUserResponse(String status, String errorMessage) {
	      super(status, errorMessage);
	  }
	  
	  public CreateUserResponse(String status, String errorMessage, int userID) {
	      super(status, errorMessage);
	      
	      this.userID = userID;
	  }

	  
	  public int getuserID()
	  {
	      return userID;
	  }
	  
	}