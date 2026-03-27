package com.licenta.backend.Model;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name="localization_history")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class LocalizationRecord {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String uploaderId;
    private LocalDateTime uploadDateTime;
    private String status;
}
