package com.licenta.backend.Facades.Implementations;

import com.licenta.backend.Facades.AuthFacade;
import com.licenta.backend.Model.UserModel;
import com.licenta.backend.Service.AuthService;
import com.licenta.backend.dto.AuthRequest;
import com.licenta.backend.dto.AuthResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;

@Component
@RequiredArgsConstructor
public class AuthFacadeImpl implements AuthFacade {
    private final AuthService authService;
    @Override
    public AuthResponse login(AuthRequest request) throws Exception {
        UserModel userModel=authService.authenticateUser(request.getUsername(), request.getPassword());
        return new AuthResponse(userModel.getId(), userModel.getUsername(), "Login successful!!");
    }

    @Override
    public AuthResponse register(AuthRequest request) throws Exception {
        UserModel userModel=authService.registerUser(request.getUsername(), request.getPassword());
        return new AuthResponse(userModel.getId(), userModel.getUsername(), "Register successful!");
    }
}
