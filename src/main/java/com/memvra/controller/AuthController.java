package com.memvra.controller;

import com.memvra.model.JwtAuthenticationResponse;
import com.memvra.model.LoginRequest;
import com.memvra.model.SignupRequest;
import com.memvra.service.AuthService;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/v1/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/signup")
    public ResponseEntity<Void> signup(@Valid @RequestBody SignupRequest request) {
        authService.registerUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).build();
    }

    @PostMapping("/login")
    public ResponseEntity<JwtAuthenticationResponse> login(
            @Valid @RequestBody LoginRequest request,
            HttpServletResponse response) {
        
        JwtAuthenticationResponse authResponse = authService.authenticateUser(request);
        
        // Set JWT as httpOnly cookie (XSS protection)
        Cookie jwtCookie = new Cookie("jwt", authResponse.getAccessToken());
        jwtCookie.setHttpOnly(true);  // Cannot be accessed by JavaScript
        jwtCookie.setSecure(false);     // Set to true in production with HTTPS
        jwtCookie.setPath("/");
        jwtCookie.setMaxAge(24 * 60 * 60); // 24 hours
        jwtCookie.setAttribute("SameSite", "Strict"); // CSRF protection
        
        response.addCookie(jwtCookie);
        
        // Still return in response for initial login feedback
        return ResponseEntity.ok(authResponse);
    }

    @PostMapping("/logout")
    public ResponseEntity<Void> logout(HttpServletResponse response) {
        // Clear the JWT cookie
        Cookie jwtCookie = new Cookie("jwt", null);
        jwtCookie.setHttpOnly(true);
        jwtCookie.setSecure(false);
        jwtCookie.setPath("/");
        jwtCookie.setMaxAge(0); // Expire immediately
        
        response.addCookie(jwtCookie);
        
        return ResponseEntity.noContent().build();
    }
}
