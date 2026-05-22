package com.licenta.backend.Facades;

import com.licenta.backend.dto.AuthRequest;
import com.licenta.backend.dto.AuthResponse;

public interface AuthFacade {
    AuthResponse login(AuthRequest request) throws Exception;
    AuthResponse register(AuthRequest request)  throws Exception;
}
