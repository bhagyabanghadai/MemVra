package com.compyle.memvra.service;

import org.junit.jupiter.api.Test;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.nio.charset.StandardCharsets;
import java.util.Base64;

import static org.junit.jupiter.api.Assertions.*;

public class CryptoServiceTest {

    @Test
    void signProducesExpectedHmac() throws Exception {
        String secret = "test-secret-key-123";
        CryptoService crypto = new CryptoService(secret);
        String payload = "mv-abc|content|user_input|src|agent|2025-01-01T00:00:00Z";

        byte[] sig = crypto.sign(payload);
        String actual = Base64.getEncoder().encodeToString(sig);

        Mac hmac = Mac.getInstance("HmacSHA256");
        hmac.init(new SecretKeySpec(secret.getBytes(StandardCharsets.UTF_8), "HmacSHA256"));
        String expected = Base64.getEncoder().encodeToString(hmac.doFinal(payload.getBytes(StandardCharsets.UTF_8)));

        assertEquals(expected, actual);
    }
}