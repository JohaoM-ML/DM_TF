# Comparacion distrito v2 (actual) vs SISAGRI (medido) — Fase A

Total combos Pareto-80: 33

## Conteo por estado

| Estado | Cantidad |
|---|---|
| DIFIERE_PUNTO_NUEVO | 24 |
| COINCIDE | 5 |
| SIN_EVIDENCIA | 2 |
| DIFIERE_PUNTO_EXISTENTE | 2 |

## Distritos nuevos candidatos (ordenados por produccion, requieren punto NASA nuevo)

| Region | Cultivo | Distrito actual | Distrito real (SISAGRI) | Produccion (t) | Fuente |
|---|---|---|---|---|---|
| Puno | avena_forrajera | Ayaviri | PUCARA | 1,143,212 | sisagri_excel_medido |
| Puno | alfalfa | Ilave | TARACO | 888,627 | sisagri_excel_medido |
| Ica | uva | Chincha Alta | SALAS | 799,011 | sisagri_excel_medido |
| Junin | pina | Perene | RIO NEGRO | 690,445 | sisagri_excel_medido |
| San Martin | arroz_cascara | Moyobamba | BAJO BIAVO | 662,068 | sisagri_excel_medido |
| Junin | papa | El Tambo | HUASAHUASI | 647,138 | sisagri_excel_medido |
| Piura | uva | Sullana | CASTILLA | 556,876 | sisagri_excel_medido |
| Piura | arroz_cascara | Sullana | IGNACIO ESCUDERO | 505,128 | sisagri_excel_medido |
| Ica | mandarina | Chincha Alta | EL CARMEN | 422,236 | sisagri_excel_medido |
| Piura | platano | Sullana | QUERECOTILLO | 380,603 | sisagri_excel_medido |
| La Libertad | arroz_cascara | Viru | GUADALUPE | 380,492 | sisagri_excel_medido |
| Ica | maiz_amarillo_duro | Chincha Alta | INDEPENDENCIA | 350,990 | sisagri_excel_medido |
| Ica | esparrago | Chincha Alta | SANTIAGO | 328,506 | sisagri_excel_medido |
| Junin | platano | Perene | PANGOA | 266,670 | sisagri_excel_medido |
| Ica | papa | Chincha Alta | NAZCA | 242,236 | sisagri_excel_medido |
| Ica | alfalfa | Chincha Alta | INDEPENDENCIA | 235,663 | sisagri_excel_medido |
| Ica | tomate | Chincha Alta | SALAS | 201,266 | sisagri_excel_medido |
| San Martin | maiz_amarillo_duro | Moyobamba | BAJO BIAVO | 188,958 | sisagri_excel_medido |
| Ica | palta | Chincha Alta | EL CARMEN | 125,142 | sisagri_excel_medido |
| Piura | cana_para_azucar | Sullana | JILILI | 104,422 | sisagri_excel_medido_parcial |
| Junin | cafe_pergamino | Perene | PICHANAQUI | 89,394 | sisagri_excel_medido |
| Junin | alfalfa | El Tambo | MATAHUASI | 65,140 | sisagri_excel_medido |
| Junin | avena_forrajera | El Tambo | SAN JOSE DE QUERO | 49,383 | sisagri_excel_medido |
| Junin | maiz_choclo | El Tambo | SAN AGUSTIN | 40,617 | sisagri_excel_medido |

## Casos sin evidencia o con nota especial

- **La Libertad / cana_para_azucar** (baja): SISAGRI no registra ningun tipo de cana de azucar en La Libertad (ni siquiera la variante alcohol). Candidato propuesto por Gemini (LLM, sin cifras verificadas) — Casa Grande y Laredo son zonas caneras historicas conocidas, pero no hay evidencia medida.
- **Piura / cana_para_azucar** (media): SISAGRI solo registra la variante 'CANA DE AZUCAR (ALCOHOL)', un producto secundario distinto de la industria azucarera dominante (azucar de exportacion). El distrito real calculado abajo puede no representar la zona cazucarera principal de Piura.
- **San Martin / palma_aceitera** (alta): SISAGRI no registra palma aceitera en ningun departamento del Peru (cultivo agroindustrial de gran escala, fuera del alcance de este sistema de reporte municipal). El distrito actual (Tocache) coincide con la hipotesis independiente de Gemini, asi que se mantiene sin cambios con confianza alta.