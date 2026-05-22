package com.licenta.backend.Service;

import com.licenta.backend.Model.UserModel;

public interface AuthService {
    UserModel registerUser(String username, String rawPassword) throws Exception;
    UserModel authenticateUser(String username, String rawPassword) throws Exception;
}
