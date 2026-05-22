package com.licenta.backend.Service.Implementations;

import com.licenta.backend.Model.UserModel;
import com.licenta.backend.Repository.UserRepository;
import com.licenta.backend.Service.AuthService;
import lombok.RequiredArgsConstructor;

import org.mindrot.jbcrypt.BCrypt;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class AuthServiceImpl implements AuthService {
    private final UserRepository userRepository;

    @Override
    public UserModel registerUser(String username, String rawPassword) throws Exception {
        if(userRepository.findByUsername(username).isPresent()){
            throw new Exception("User already exists");
        }
        String hashedPassword = BCrypt.hashpw(rawPassword, BCrypt.gensalt(12));
        UserModel newUser=UserModel.builder()
                .username(username)
                .password(hashedPassword)
                .build();
        return userRepository.save(newUser);
    }

    @Override
    public UserModel authenticateUser(String username, String rawPassword) throws Exception {
        Optional<UserModel> userOpt = userRepository.findByUsername(username);
        if(userOpt.isPresent()){
            UserModel user = userOpt.get();
            if(BCrypt.checkpw(rawPassword, user.getPassword())){
                return user;
            }
        }
        throw new Exception("Invalid username or password");
    }
}
