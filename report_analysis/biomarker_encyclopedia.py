"""
HexaDisease - Biomarker Encyclopedia & Plain-Language Clinical Guide
Provides comprehensive medical literacy for routine lab tests across the 6 diseases:
- Reference ranges (Min, Max, Unit)
- Physiological importance in simple plain language
- Low vs High clinical interpretation
- Early warning indicators (for catching disease early)
- Daily control strategies: Specific Foods, Recommended Fruits, Exercises, and Precautions
"""

BIOMARKER_ENCYCLOPEDIA = {
    # -------------------------------------------------------------------------
    # HEMATOLOGY & COMPLETE BLOOD COUNT (CBC) - ANEMIA & INFECTION
    # -------------------------------------------------------------------------
    "wbc": {
        "key": "wbc",
        "display_name": "White Blood Cell (WBC) Count",
        "category": "Hematology & Immune Function",
        "unit": "cells/mcL",
        "reference_min": 4500,
        "reference_max": 11000,
        "optimal_range": "4,500 - 11,000 cells/mcL",
        "importance": "White blood cells (leukocytes) are your body's immune defense soldiers. They constantly circulate in your bloodstream to detect and fight off viruses, bacteria, parasites, and internal inflammation.",
        "low_explanation": "A low WBC count (leukopenia, < 4,500) indicates your immune system may be weakened or stressed, making you more vulnerable to catching bacterial or viral infections.",
        "high_explanation": "A high WBC count (leukocytosis, > 11,000) usually means your body is actively fighting an infection, reacting to acute inflammation, intense physical stress, or an allergic response.",
        "early_warning": "In routine checkups, mild elevations (11,000 - 13,000) are very common after minor throat infections, dental inflammation, or intense workout stress. No need to panic; look for signs of simple physical stress or seasonal colds.",
        "how_to_control": {
            "diet_actions": "Eat immune-regulating antioxidant foods. Emphasize garlic, ginger, turmeric, leafy greens, and probiotic yogurt.",
            "recommended_fruits": [
                "Citrus Fruits (Oranges, Lemons, Grapefruits) - rich in Vitamin C to stimulate healthy white cell production",
                "Papaya & Kiwi - packed with folate and immune enzymes",
                "Blueberries & Blackberries - high anthocyanin antioxidants that reduce systemic inflammation"
            ],
            "exercises": "Moderate brisk walking or cycling 20-30 minutes daily. Avoid excessive exhausting overtraining when WBC is slightly elevated.",
            "daily_precautions": "Stay well-hydrated (2.5L clean water daily), maintain 7-8 hours of sleep, and practice good hand hygiene."
        }
    },
    "rbc": {
        "key": "rbc",
        "display_name": "Red Blood Cell (RBC) Count",
        "category": "Hematology & Oxygen Delivery",
        "unit": "million/mcL",
        "reference_min": 4.2,
        "reference_max": 5.9,
        "optimal_range": "4.2 - 5.9 million/mcL",
        "importance": "Red blood cells carry hemoglobin, acting as oxygen delivery trucks from your lungs to your brain, heart, muscles, and every organ.",
        "low_explanation": "Low RBC (< 4.2) indicates anemia, meaning your tissues are starving for adequate oxygen, resulting in fatigue, pale skin, and shortness of breath.",
        "high_explanation": "High RBC (> 5.9) can signal dehydration, chronic sleep apnea, low blood oxygen levels (e.g., in smokers), or bone marrow overproduction.",
        "early_warning": "Early drops cause subtle morning lethargy, cold hands/feet, and poor workout stamina before full clinical anemia develops.",
        "how_to_control": {
            "diet_actions": "Consume iron-dense foods (spinach, lentils, beets, pumpkin seeds, lean meats) paired with Vitamin C to multiply iron absorption.",
            "recommended_fruits": [
                "Pomegranates - powerful natural booster of red blood cell counts and hemoglobin synthesis",
                "Dried Dates & Figs - dense in non-heme iron and minerals",
                "Prunes & Raisins - stimulate bone marrow oxygen transport"
            ],
            "exercises": "Aerobic workouts (swimming, light jogging, brisk walking) 3-4 days a week to stimulate erythropoietin.",
            "daily_precautions": "Avoid drinking black tea or coffee right with meals, as tannins inhibit iron absorption by up to 60%."
        }
    },
    "hemo": {
        "key": "hemo",
        "display_name": "Hemoglobin (Hb)",
        "category": "Hematology & Oxygen Delivery",
        "unit": "g/dL",
        "reference_min": 12.0,
        "reference_max": 17.5,
        "optimal_range": "12.0 - 15.5 g/dL (Females), 13.5 - 17.5 g/dL (Males)",
        "importance": "Hemoglobin is the iron-rich protein inside red blood cells that magnetically binds oxygen molecules and transports them to every cell in your body.",
        "low_explanation": "Low hemoglobin (< 12.0) is the hallmark diagnostic definition of anemia. Your organs receive insufficient oxygen, causing brain fog, dizziness, fatigue, and heart palpitations.",
        "high_explanation": "High hemoglobin (> 17.5) thickens blood viscosity, increasing cardiovascular workload and clot risks.",
        "early_warning": "Early stage anemia (Hb 11.0 - 11.9) is easily reversible with nutritional corrections before needing pharmaceutical intravenous infusions.",
        "how_to_control": {
            "diet_actions": "Eat cooked spinach, moringa leaves, black beans, chickpeas, organic eggs, and beetroot salads.",
            "recommended_fruits": [
                "Pomegranate - highest clinically proven fruit to rapidly elevate hemoglobin levels",
                "Amla (Indian Gooseberry) - astronomical Vitamin C content that accelerates iron absorption",
                "Apples & Watermelon - provide natural iron along with optimal cellular hydration"
            ],
            "exercises": "Gentle daily 20-30 minute walks. If fatigued, do not engage in heavy weightlifting until Hb stabilizes above 12.0 g/dL.",
            "daily_precautions": "Take iron supplements only after food, cook in cast-iron cookware, and re-test within 60 days."
        }
    },
    "platelets": {
        "key": "platelets",
        "display_name": "Platelet Count",
        "category": "Hematology & Clotting",
        "unit": "x10^3/mcL",
        "reference_min": 150,
        "reference_max": 450,
        "optimal_range": "150 - 450 x10^3/mcL",
        "importance": "Platelets are microscopic disc-shaped blood cell fragments that rush to seal cuts, stop bleeding, and assist vascular wound healing.",
        "low_explanation": "Low platelets (thrombocytopenia, < 150) increase bruising and prolonged bleeding from small scratches.",
        "high_explanation": "Elevated platelets (thrombocytosis, > 450) can indicate systemic inflammation or elevate clotting hazards.",
        "early_warning": "Mild dips (130 - 149) often follow viral fevers (like dengue or flu) and naturally rebound in 1-2 weeks.",
        "how_to_control": {
            "diet_actions": "Consume foods rich in folate and Vitamin B12: green leafy vegetables, fortified nutritional yeast, and beans.",
            "recommended_fruits": [
                "Papaya & Papaya Leaf Extract - widely documented to support platelet recovery",
                "Berries (Strawberries, Raspberries) - packed with Vitamin C and anti-inflammatory flavonoids",
                "Kiwi Fruit - abundant in Vitamin C and essential trace minerals"
            ],
            "exercises": "Low-impact physical movements (walking, yoga). Avoid contact sports if platelets are below 100.",
            "daily_precautions": "Avoid unprescribed aspirin or NSAIDs which thin the blood further."
        }
    },

    # -------------------------------------------------------------------------
    # METABOLIC & GLYCEMIC REGULATION - DIABETES
    # -------------------------------------------------------------------------
    "fasting_glucose": {
        "key": "fasting_glucose",
        "display_name": "Fasting Blood Glucose",
        "category": "Metabolism & Glycemic Control",
        "unit": "mg/dL",
        "reference_min": 70,
        "reference_max": 99,
        "optimal_range": "70 - 99 mg/dL",
        "importance": "Measures your baseline blood sugar level after an 8 to 12 hour overnight fast. It is the primary early indicator of metabolic health and pancreatic insulin sensitivity.",
        "low_explanation": "Low fasting glucose (< 70 mg/dL, hypoglycemia) causes shaky hands, sweating, irritability, anxiety, and dizziness.",
        "high_explanation": "Fasting glucose 100 - 125 mg/dL indicates Prediabetes (Impaired Fasting Glucose). Readings >= 126 mg/dL on two tests confirm Type 2 Diabetes.",
        "early_warning": "THE CRITICAL EARLY REVERSIBLE WINDOW! A reading between 100 - 115 mg/dL is an early wake-up call: your pancreas is producing insulin, but muscle cells are resisting it. It can be 100% reversed with simple food and walking habits!",
        "how_to_control": {
            "diet_actions": "Switch immediately to low-glycemic foods. Replace white rice, white bread, and sugar with oats, quinoa, chia seeds, and raw salads before meals.",
            "recommended_fruits": [
                "Green Apples & Berries (Blueberries, Blackberries) - low glycemic load, rich in pectin and anthocyanins that slow sugar absorption",
                "Cherries - lowest glycemic index of all stone fruits (GI 22)",
                "Guava & Indian Jamun (Black Plum) - proven traditional fruits that improve insulin receptor sensitivity"
            ],
            "exercises": "A 10-15 minute gentle walk immediately after meals ('postprandial walking') utilizes muscle contractions to soak up glucose without insulin.",
            "daily_precautions": "Stop late-night snacking after 8:00 PM to give your liver a full 12-hour metabolic rest period."
        }
    },
    "hba1c": {
        "key": "hba1c",
        "display_name": "Glycated Hemoglobin (HbA1c)",
        "category": "Metabolism & Glycemic Control",
        "unit": "%",
        "reference_min": 4.0,
        "reference_max": 5.6,
        "optimal_range": "< 5.7%",
        "importance": "HbA1c provides a true 90-day three-month average of your blood glucose levels by measuring the percentage of hemoglobin coated with sugar molecules.",
        "low_explanation": "Very low HbA1c (< 4.5%) is rare and may reflect hemolytic anemia or recurrent severe hypoglycemic episodes.",
        "high_explanation": "HbA1c 5.7% - 6.4% confirms Prediabetes. HbA1c >= 6.5% confirms clinical Diabetes.",
        "early_warning": "If your HbA1c is 5.7% - 6.0%, you have caught diabetes years before any permanent organ damage occurs! Daily lifestyle changes can bring it back below 5.5%.",
        "how_to_control": {
            "diet_actions": "Cut out all liquid sugars (colas, sweetened juices, sweet tea). Practice the plate method: half plate vegetables, one-quarter lean protein, one-quarter complex carbs.",
            "recommended_fruits": [
                "Avocado - healthy monounsaturated fat with virtually zero net carbs",
                "Blueberries & Raspberries - satisfy sweet cravings with high soluble fiber",
                "Grapefruit - containing naringenin, which promotes carbohydrate metabolism"
            ],
            "exercises": "Combine aerobic exercise (150 min/week) with 2 days of bodyweight or resistance training to build glucose-burning muscle mass.",
            "daily_precautions": "Re-test HbA1c strictly every 90 days to verify whether your lifestyle interventions are lowering the line."
        }
    },

    # -------------------------------------------------------------------------
    # RENAL & KIDNEY FUNCTION - CHRONIC KIDNEY DISEASE (CKD)
    # -------------------------------------------------------------------------
    "serum_creatinine": {
        "key": "serum_creatinine",
        "display_name": "Serum Creatinine",
        "category": "Renal & Kidney Filtration",
        "unit": "mg/dL",
        "reference_min": 0.6,
        "reference_max": 1.2,
        "optimal_range": "0.6 - 1.2 mg/dL",
        "importance": "Creatinine is a natural waste breakdown product of muscle energy metabolism. Healthy kidneys continuously filter 100% of it out through urine.",
        "low_explanation": "Low creatinine (< 0.6) is generally harmless and typically indicates low muscle mass, advanced age, or a very low-protein vegetarian diet.",
        "high_explanation": "Elevated creatinine (> 1.2) means your kidneys' microscopic nephron filters are strained or losing filtration efficiency, allowing waste to accumulate in the blood.",
        "early_warning": "Early renal stress appears as creatinine hovering between 1.2 - 1.4 mg/dL. Often caused by mild chronic dehydration, heavy gym creatine supplements, or unmanaged high blood pressure.",
        "how_to_control": {
            "diet_actions": "Reduce excessive red meat and synthetic creatine powder. Lower sodium (salt) intake to under 2,000 mg/day to relieve glomerular pressure.",
            "recommended_fruits": [
                "Cranberries & Blueberries - protect urinary tract and shield kidney filtering cells with proanthocyanidins",
                "Watermelon - high water content and natural diuretic action that gently flushes urea without kidney strain",
                "Apples - low potassium, kidney-friendly fruit rich in anti-inflammatory fiber"
            ],
            "exercises": "Light to moderate walking and stretching. Avoid extreme, dehydrating rhabdomyolysis-inducing crossfit sessions.",
            "daily_precautions": "Drink 2.5 to 3 liters of water daily. Avoid frequent use of over-the-counter painkillers (ibuprofen, naproxen) which are toxic to kidneys."
        }
    },
    "blood_urea": {
        "key": "blood_urea",
        "display_name": "Blood Urea / Blood Urea Nitrogen (BUN)",
        "category": "Renal & Protein Metabolism",
        "unit": "mg/dL",
        "reference_min": 15,
        "reference_max": 45,
        "optimal_range": "15 - 45 mg/dL",
        "importance": "Measures the amount of urea nitrogen in your blood, created when your liver breaks down dietary proteins. Healthy kidneys remove it cleanly.",
        "low_explanation": "Low blood urea (< 15) is uncommon and usually relates to very low dietary protein intake or liver insufficiency.",
        "high_explanation": "High urea (> 45) indicates decreased renal clearance, acute dehydration, severe fever, or very high protein catabolism.",
        "early_warning": "If urea is high while creatinine is normal, dehydration is the 90% likely culprit! Re-hydrating with water often normalizes it within 48 hours.",
        "how_to_control": {
            "diet_actions": "Balance daily protein intake (0.8 - 1.0 g per kg body weight). Emphasize plant proteins over heavy commercial whey shakes.",
            "recommended_fruits": [
                "Cucumbers & Watermelon - excellent natural electrolytes that assist urea flushing",
                "Pineapple - contains bromelain, which aids protein digestion",
                "Pears - gentle on kidneys with low nitrogen load"
            ],
            "exercises": "Moderate walking, swimming, and stationary cycling.",
            "daily_precautions": "Hydrate consistently throughout the day; do not wait until you feel thirsty."
        }
    },
    "urine_albumin": {
        "key": "urine_albumin",
        "display_name": "Urine Albumin / Proteinuria",
        "category": "Renal Glomerular Barrier",
        "unit": "mg/L",
        "reference_min": 0,
        "reference_max": 30,
        "optimal_range": "< 30 mg/L (Negative / Trace)",
        "importance": "Albumin is an essential blood protein that should NEVER leak through healthy kidney filters into urine.",
        "low_explanation": "Zero albumin in urine is completely normal and optimal.",
        "high_explanation": "Presence of albumin in urine (microalbuminuria 30 - 300 mg/L) is the earliest clinical sign of diabetic or hypertensive kidney damage.",
        "early_warning": "Catching microalbuminuria early allows complete prevention of chronic kidney disease (CKD) before creatinine even starts rising!",
        "how_to_control": {
            "diet_actions": "Strictly restrict dietary salt to 1.5 teaspoons daily. Manage blood pressure strictly below 130/80 mmHg.",
            "recommended_fruits": [
                "Cranberries & Red Grapes - rich in resveratrol to protect the delicate glomerular podocyte barrier",
                "Strawberries - packed with antioxidants that protect kidney capillary lining"
            ],
            "exercises": "Daily 30-minute moderate aerobic exercise to keep vascular tension low.",
            "daily_precautions": "Have your physician screen urine albumin-to-creatinine ratio (uACR) annually if you have high BP or prediabetes."
        }
    },

    # -------------------------------------------------------------------------
    # CARDIOVASCULAR & CEREBROVASCULAR - STROKE & HYPERTENSION
    # -------------------------------------------------------------------------
    "systolic_bp": {
        "key": "systolic_bp",
        "display_name": "Systolic Blood Pressure",
        "category": "Vascular Hemodynamics & Stroke Risk",
        "unit": "mmHg",
        "reference_min": 90,
        "reference_max": 120,
        "optimal_range": "90 - 119 mmHg",
        "importance": "Measures the maximum arterial pressure exerted against your blood vessel walls each time your heart beats and pumps blood.",
        "low_explanation": "Low systolic BP (< 90 mmHg, hypotension) causes dizziness when standing quickly, lightheadedness, and fainting.",
        "high_explanation": "120 - 129 mmHg is Elevated BP. 130 - 139 mmHg is Stage 1 Hypertension. >= 140 mmHg is Stage 2 Hypertension, dramatically multiplying stroke risks.",
        "early_warning": "Elevated BP (120 - 129 mmHg) produces zero symptoms ('the silent killer') but silently stretches arterial walls. It is 100% reversible with sodium cuts and potassium foods!",
        "how_to_control": {
            "diet_actions": "Adopt the DASH diet (Dietary Approaches to Stop Hypertension): cut table salt, avoid canned/processed foods, and boost dietary potassium and magnesium.",
            "recommended_fruits": [
                "Bananas & Cantaloupe - rich in potassium, which naturally counters sodium and relaxes vascular muscle walls",
                "Pomegranate - clinically shown to inhibit ACE enzyme and lower systolic pressure",
                "Watermelon - contains L-citrulline, an amino acid that converts to nitric oxide to dilate blood vessels"
            ],
            "exercises": "Aerobic workouts: 30 minutes of brisk walking, swimming, or cycling 5 days weekly can lower systolic BP by 5-8 mmHg.",
            "daily_precautions": "Practice 5 minutes of slow diaphragmatic deep breathing twice daily (slow 6 breaths per minute) to calm sympathetic vascular tone."
        }
    },
    "diastolic_bp": {
        "key": "diastolic_bp",
        "display_name": "Diastolic Blood Pressure",
        "category": "Vascular Hemodynamics & Stroke Risk",
        "unit": "mmHg",
        "reference_min": 60,
        "reference_max": 80,
        "optimal_range": "60 - 79 mmHg",
        "importance": "Measures the resting arterial pressure in your blood vessels between heartbeats while your cardiac muscle pauses to refill with blood.",
        "low_explanation": "Low diastolic BP (< 60 mmHg) can lead to insufficient coronary blood flow during diastole.",
        "high_explanation": "80 - 89 mmHg is Stage 1 Hypertension. >= 90 mmHg is Stage 2 Hypertension, indicating high peripheral arterial vascular resistance.",
        "early_warning": "A diastolic reading of 80 - 85 mmHg often reflects stress, poor sleep, or excess caffeine, serving as an early wake-up signal.",
        "how_to_control": {
            "diet_actions": "Reduce refined salt, limit caffeine to mornings only, and consume magnesium-rich almonds, pumpkin seeds, and spinach.",
            "recommended_fruits": [
                "Avocado & Kiwi - deliver magnesium and potassium for resting arterial dilation",
                "Oranges - high hesperidin flavonoid content that improves endothelial elasticity"
            ],
            "exercises": "Consistent rhythmic walking or light jogging. Avoid isometric heavy straining if diastolic is over 90.",
            "daily_precautions": "Prioritize 7-8 hours of continuous sleep; sleep deprivation directly spikes resting diastolic pressure."
        }
    },

    # -------------------------------------------------------------------------
    # CARDIAC FUNCTION & MYOCARDIAL INTEGRITY - HEART FAILURE
    # -------------------------------------------------------------------------
    "ejection_fraction": {
        "key": "ejection_fraction",
        "display_name": "Left Ventricular Ejection Fraction (LVEF)",
        "category": "Cardiology & Heart Pumping",
        "unit": "%",
        "reference_min": 50,
        "reference_max": 70,
        "optimal_range": "50% - 70%",
        "importance": "The percentage of blood leaving your heart's main pumping chamber (left ventricle) with each contraction. It is the gold-standard metric of myocardial pump strength.",
        "low_explanation": "Ejection fraction 41% - 49% indicates mildly reduced heart failure (Borderline). EF <= 40% indicates Heart Failure with Reduced Ejection Fraction (HFrEF).",
        "high_explanation": "EF above 70% can occasionally reflect hyperdynamic states like severe hyperthyroidism.",
        "early_warning": "Early pre-heart failure (EF 45% - 50%) often manifests subtly as getting unusually out of breath when climbing 2 flights of stairs.",
        "how_to_control": {
            "diet_actions": "Strictly limit dietary sodium to 1,500 mg daily to prevent fluid retention. Moderate total fluid intake if advised by cardiologist.",
            "recommended_fruits": [
                "Berries (Blueberries, Blackberries) - packed with polyphenols that support myocardial endothelial function",
                "Pomegranates - proven to improve coronary blood flow and reduce arterial plaque oxidation",
                "Papaya & Apples - gentle fiber without fluid loading"
            ],
            "exercises": "Doctor-supervised cardiac rehabilitation or gentle graduated walking 15-20 minutes daily. Stop immediately if feeling dizzy or chest tightness.",
            "daily_precautions": "Weigh yourself every morning; a sudden gain of 2-3 pounds in 24 hours warns of fluid retention before severe breathlessness strikes."
        }
    },
    "cpk": {
        "key": "cpk",
        "display_name": "Creatine Phosphokinase (CPK / CK)",
        "category": "Cardiology & Muscle Stress",
        "unit": "mcg/L",
        "reference_min": 30,
        "reference_max": 200,
        "optimal_range": "30 - 200 mcg/L",
        "importance": "An essential cellular enzyme found in your heart muscle, skeletal muscle, and brain that helps generate cellular energy (ATP).",
        "low_explanation": "Low CPK is usually clinically insignificant and can correlate with low physical muscle mass.",
        "high_explanation": "Elevated CPK (> 200) signals muscle cell leakage resulting from intense physical strain, muscle trauma, statin medication sensitivity, or acute myocardial injury.",
        "early_warning": "Routine checkup elevations (250 - 500) frequently occur 24-48 hours after heavy gym workouts or unaccustomed marathon running. No need to panic if chest pain is absent!",
        "how_to_control": {
            "diet_actions": "Drink abundant fluids to protect your kidneys from myoglobin breakdown. Consume anti-inflammatory turmeric (curcumin) and tart cherry extract.",
            "recommended_fruits": [
                "Tart Cherries - clinically proven to reduce muscle damage markers and accelerate CPK recovery",
                "Pineapple (Bromelain) - natural enzyme that eases systemic muscle soreness and breakdown",
                "Bananas - replenish electrolytes to stop muscle cramping"
            ],
            "exercises": "Take 2-3 full rest days after intense training. Replace strenuous weights with gentle walking or sauna hydration.",
            "daily_precautions": "If you take cholesterol-lowering statin pills and notice muscle pain alongside high CPK, consult your doctor about dosage adjustment."
        }
    },
    "total_cholesterol": {
        "key": "total_cholesterol",
        "display_name": "Total Cholesterol",
        "category": "Lipids & Vascular Health",
        "unit": "mg/dL",
        "reference_min": 125,
        "reference_max": 200,
        "optimal_range": "< 200 mg/dL",
        "importance": "Total cholesterol measures the complete sum of circulating lipids in your bloodstream, including protective HDL and atherogenic LDL/VLDL particles.",
        "low_explanation": "Very low cholesterol (< 120 mg/dL) can impair cellular membrane stability, hormone production, and fat-soluble vitamin absorption.",
        "high_explanation": "Elevated cholesterol (> 200 mg/dL) leads to microscopic lipid plaque accumulation inside your arterial walls (atherosclerosis), increasing stroke and cardiac risk.",
        "early_warning": "Borderline levels (200 - 239 mg/dL) are 100% reversible through dietary fiber (soluble pectin) and eliminating hydrogenated trans-fats before arterial stiffening begins.",
        "how_to_control": {
            "diet_actions": "Eat soluble fiber foods: rolled oats, barley, chia seeds, and ground flaxseed. Cook with extra virgin olive oil instead of butter or palm oil.",
            "recommended_fruits": [
                "Apples (Pectin) - binds bile acids in the gut to draw excess cholesterol out of the bloodstream",
                "Avocado - delivers heart-healthy monounsaturated fats that lower LDL and raise protective HDL",
                "Citrus Fruits (Oranges, Grapefruits) - rich in hesperidin and soluble fiber to prevent arterial plaque formation"
            ],
            "exercises": "30 to 45 minutes of moderate aerobic cardio (brisk walking, swimming, cycling) 5 days a week.",
            "daily_precautions": "Avoid processed baked pastries, deep-fried snacks, and vanaspati ghee containing trans-fatty acids."
        }
    },
    "hematocrit": {
        "key": "hematocrit",
        "display_name": "Hematocrit / Packed Cell Volume (PCV)",
        "category": "Hematology & Oxygen Delivery",
        "unit": "%",
        "reference_min": 36.0,
        "reference_max": 50.0,
        "optimal_range": "36.0 - 46.0% (Females), 41.0 - 50.0% (Males)",
        "importance": "Hematocrit measures the proportion of your total blood volume made up of red blood cells. It reflects both oxygen-carrying capacity and whole blood viscosity.",
        "low_explanation": "Low hematocrit (< 36%) confirms anemia or blood loss, resulting in tissue hypoxia, cognitive fatigue, cold extremities, and shortness of breath on exertion.",
        "high_explanation": "High hematocrit (> 50%) thickens your blood like sludge, placing excessive workload on the heart and drastically increasing the hazard of vascular clots and stroke.",
        "early_warning": "Slight low values (32 - 35%) indicate early-stage iron or folate depletion that can be fully corrected through dietary fruit and greens before severe clinical anemia develops.",
        "how_to_control": {
            "diet_actions": "Incorporate iron-rich lentils, spinach, moringa, beetroot, and sesame seeds paired with Vitamin C to multiply bio-availability.",
            "recommended_fruits": [
                "Pomegranates - stimulates erythropoiesis (red blood cell production) and elevates hematocrit levels naturally",
                "Dried Black Raisins & Figs - dense non-heme iron and copper sources required for red cell maturation",
                "Beetroot & Amla Juice - traditional hematinic booster promoting healthy packed cell volume"
            ],
            "exercises": "Gentle daily walking and diaphragmatic breathing to stimulate bone marrow oxygen transport.",
            "daily_precautions": "Maintain adequate hydration (2.5L clean water daily), as mild dehydration can artificially elevate hematocrit on lab reports."
        }
    },
    "serum_sodium": {
        "key": "serum_sodium",
        "display_name": "Serum Sodium",
        "category": "Electrolytes & Fluid Balance",
        "unit": "mmol/L",
        "reference_min": 135,
        "reference_max": 145,
        "optimal_range": "135 - 145 mmol/L",
        "importance": "Sodium is the primary extracellular electrolyte that regulates total body water, cellular hydration, blood pressure, and neuromuscular signaling.",
        "low_explanation": "Low sodium (hyponatremia, < 135 mmol/L) causes cellular swelling, headache, nausea, brain fog, and muscle weakness. Frequent in congestive heart failure and over-diuresis.",
        "high_explanation": "High sodium (hypernatremia, > 145 mmol/L) signals severe dehydration or fluid loss, causing intense thirst, arterial constriction, and confusion.",
        "early_warning": "Mild dips (130 - 134 mmol/L) in heart failure patients warn of fluid overload and neurohormonal activation before noticeable leg swelling occurs.",
        "how_to_control": {
            "diet_actions": "Maintain moderate salt consumption without extreme sodium depletion. Follow your doctor's fluid limit if you have heart or kidney failure.",
            "recommended_fruits": [
                "Coconut Water - natural isotonic electrolyte beverage that gently restores balanced extracellular minerals",
                "Watermelon - provides natural cellular hydration without sodium spiking",
                "Pears - soothing hydration with low sodium and gentle mineral balance"
            ],
            "exercises": "Light aerobic movement and gentle stretching. Avoid excessive sweating in high heat when sodium is low.",
            "daily_precautions": "Do not drink massive quantities of plain water rapidly, as this can dilute serum sodium dangerously."
        }
    },
    "heart_rate": {
        "key": "heart_rate",
        "display_name": "Resting Heart Rate / Pulse",
        "category": "Cardiovascular & Hemodynamics",
        "unit": "bpm",
        "reference_min": 60,
        "reference_max": 90,
        "optimal_range": "60 - 80 bpm",
        "importance": "Measures the number of heart beats per minute at rest. It serves as a direct barometer of cardiovascular fitness, autonomic nervous system tone, and cardiac workload.",
        "low_explanation": "A slow heart rate (< 60 bpm, bradycardia) is common and healthy in trained athletes, but in unconditioned individuals may indicate sinus node fatigue or thyroid underactivity.",
        "high_explanation": "A high resting heart rate (> 90-100 bpm, tachycardia) indicates sympathetic overdrive, systemic inflammation, chronic stress, dehydration, anemia, or maternal vascular strain.",
        "early_warning": "Resting pulse steadily creeping from 70 to 88+ bpm over months is an early signal of physical deconditioning, high stress, or borderline hypertension.",
        "how_to_control": {
            "diet_actions": "Eliminate excess caffeine, energy drinks, and nicotine. Increase magnesium-dense foods like leafy greens, pumpkin seeds, and almonds to relax the cardiac pacemaker.",
            "recommended_fruits": [
                "Bananas & Oranges - high potassium content counteracts adrenaline and stabilizes myocardial electrical impulses",
                "Blueberries - rich in polyphenols that improve vagal tone and lower resting pulse",
                "Passion Fruit & Cherries - natural relaxing antioxidants that reduce cardiac sympathetic strain"
            ],
            "exercises": "Regular 30-minute zone-2 aerobic walks, swimming, and slow 4-7-8 parasympathetic deep breathing.",
            "daily_precautions": "Measure your pulse first thing in the morning while still lying in bed for the most accurate resting baseline."
        }
    },
    "bmi": {
        "key": "bmi",
        "display_name": "Body Mass Index (BMI)",
        "category": "Metabolism & Body Composition",
        "unit": "kg/m2",
        "reference_min": 18.5,
        "reference_max": 24.9,
        "optimal_range": "18.5 - 24.9 kg/m2",
        "importance": "A screening metric relating height to weight that estimates total body fat and metabolic disease risk, particularly visceral fat around vital abdominal organs.",
        "low_explanation": "Underweight (BMI < 18.5) increases risks of immune vulnerability, nutrient deficiencies, and osteoporosis.",
        "high_explanation": "Overweight (BMI 25.0 - 29.9) and Obesity (BMI >= 30.0) significantly accelerate insulin resistance, arterial hypertension, chronic kidney strain, and stroke risk.",
        "early_warning": "Creeping from BMI 24 to 26 is the prime window to act! A modest 5% weight reduction reverses prediabetes risk by over 58% according to landmark clinical trials.",
        "how_to_control": {
            "diet_actions": "Prioritize high-volume, low-calorie nutrient-dense whole foods: salads, broths, whole grains, and lean proteins. Eliminate liquid sugars.",
            "recommended_fruits": [
                "Apples & Pears - high water and pectin fiber that triggers satiety hormones and reduces overall calorie consumption",
                "Grapefruit - proven to assist insulin sensitivity and metabolic rate",
                "Berries - low calorie density with high antioxidant load for healthy weight management"
            ],
            "exercises": "Daily 8,000 to 10,000 steps brisk walking combined with two weekly resistance sessions to preserve fat-burning muscle mass.",
            "daily_precautions": "Measure waist circumference alongside BMI: waist should ideally remain under 35 inches for women and under 40 inches for men."
        }
    },
    "body_temperature": {
        "key": "body_temperature",
        "display_name": "Body Temperature",
        "category": "Physiology & Hemodynamics",
        "unit": "°F",
        "reference_min": 97.6,
        "reference_max": 99.1,
        "optimal_range": "98.0 - 98.8 °F (36.7 - 37.1 °C)",
        "importance": "Measures internal core thermal regulation, controlled by the hypothalamus. Vital for enzymatic functions and maternal metabolic monitoring.",
        "low_explanation": "Low body temperature (< 97.0 °F, hypothermia) impairs cellular enzyme kinetics and can signal hypothyroidism, acute shock, or environmental exposure.",
        "high_explanation": "Elevated temperature (> 99.5 °F low-grade, > 100.4 °F fever) indicates an active immune response to infection, systemic inflammation, or heat exhaustion.",
        "early_warning": "Persistent low-grade fever during pregnancy or routine checkup indicates an active subclinical infection or inflammatory focus that needs evaluation.",
        "how_to_control": {
            "diet_actions": "Consume hydrating cooling fluids, coconut water, broths, and fresh light meals. Avoid heavy spicy or oily foods during thermal elevation.",
            "recommended_fruits": [
                "Watermelon & Musk Melon - deeply hydrating cooling fruits that replenish fluids during thermal stress",
                "Pomegranates - natural anti-pyretic antioxidants that soothe internal inflammation",
                "Oranges & Sweet Limes - rich in Vitamin C and electrolytes to support active immune recovery"
            ],
            "exercises": "Complete physical rest until temperature normalizes. Do not engage in strenuous workouts while febrile.",
            "daily_precautions": "Drink plenty of room-temperature clean fluids and use cool forehead compresses if temperature rises above 100 °F."
        }
    }
}

def get_biomarker_info(key):
    """Retrieves plain-language educational breakdown for any laboratory parameter."""
    clean_k = key.lower().strip().replace(" ", "_")
    
    # 1. Direct match
    if clean_k in BIOMARKER_ENCYCLOPEDIA:
        return BIOMARKER_ENCYCLOPEDIA[clean_k]
        
    # 2. Key aliases
    alias_map = {
        "glucose": "fasting_glucose",
        "fpg": "fasting_glucose",
        "sugar": "fasting_glucose",
        "blood_sugar": "fasting_glucose",
        "bs": "fasting_glucose",
        "pp_glucose": "fasting_glucose",
        "random_glucose": "fasting_glucose",
        "a1c": "hba1c",
        "glycated_hemoglobin": "hba1c",
        "creatinine": "serum_creatinine",
        "sc": "serum_creatinine",
        "cr": "serum_creatinine",
        "urea": "blood_urea",
        "bu": "blood_urea",
        "bun": "blood_urea",
        "hb": "hemo",
        "hemoglobin": "hemo",
        "haemoglobin": "hemo",
        "white_blood_cells": "wbc",
        "white_blood_cell": "wbc",
        "leukocytes": "wbc",
        "wbcc": "wbc",
        "red_blood_cells": "rbc",
        "rbcc": "rbc",
        "platelet": "platelets",
        "plt": "platelets",
        "systolic": "systolic_bp",
        "systolicbp": "systolic_bp",
        "diastolic": "diastolic_bp",
        "diastolicbp": "diastolic_bp",
        "bp": "systolic_bp",
        "ef": "ejection_fraction",
        "lvef": "ejection_fraction",
        "ck": "cpk",
        "creatine_kinase": "cpk",
        "albumin": "urine_albumin",
        "al": "urine_albumin",
        "proteinuria": "urine_albumin",
        "cholesterol": "total_cholesterol",
        "total_cholesterol": "total_cholesterol",
        "pcv": "hematocrit",
        "packed_cell_volume": "hematocrit",
        "sodium": "serum_sodium",
        "serum_sodium": "serum_sodium",
        "pulse": "heart_rate",
        "heartrate": "heart_rate",
        "temp": "body_temperature",
        "temperature": "body_temperature",
        "bodytemp": "body_temperature"
    }
    
    if clean_k in alias_map:
        return BIOMARKER_ENCYCLOPEDIA[alias_map[clean_k]]
        
    for ak, target in alias_map.items():
        if ak in clean_k or clean_k in ak:
            return BIOMARKER_ENCYCLOPEDIA[target]
            
    return None

def explain_parameter_level(parameter_key, value):
    """
    Evaluates current value vs reference range, computes delta,
    and returns a user-friendly status, level classification, and actionable control tips.
    """
    info = get_biomarker_info(parameter_key)
    if not info:
        return {
            "parameter": parameter_key,
            "value": value,
            "status": "DETECTED",
            "level": "Within Observed Range",
            "explanation": f"Measured at {value}. Consult standard clinical reference ranges.",
            "importance": "Clinical biomarker monitored during comprehensive health screening.",
            "recommended_fruits": ["Apples", "Pomegranates", "Berries"],
            "how_to_control": "Maintain balanced daily hydration, dietary variety, and 30 minutes of regular activity."
        }
        
    val_num = float(value) if isinstance(value, (int, float)) else None
    if val_num is None:
        try:
            val_num = float(str(value).replace("%", "").replace("mmHg", "").strip())
        except Exception:
            val_num = None

    ref_min = info["reference_min"]
    ref_max = info["reference_max"]
    
    if val_num is not None:
        if val_num < ref_min:
            delta = round(ref_min - val_num, 2)
            pct = round((delta / ref_min) * 100, 1)
            level = f"Low ({delta} {info['unit']} below normal minimum, -{pct}%)"
            status = "LOW"
            clinical_why = info["low_explanation"]
        elif val_num > ref_max:
            delta = round(val_num - ref_max, 2)
            pct = round((delta / ref_max) * 100, 1)
            level = f"High (+{delta} {info['unit']} above normal maximum, +{pct}%)"
            status = "HIGH"
            clinical_why = info["high_explanation"]
        else:
            level = f"Optimal (Within healthy reference limits: {ref_min} - {ref_max} {info['unit']})"
            status = "OPTIMAL"
            clinical_why = "Your reading is within healthy physiological boundaries. Great job!"
    else:
        status = "MEASURED"
        level = "Laboratory Observation"
        clinical_why = "Observed lab value."

    return {
        "key": info["key"],
        "parameter": info["display_name"],
        "category": info["category"],
        "current_value": value,
        "unit": info["unit"],
        "optimal_range": info["optimal_range"],
        "status": status,
        "level_assessment": level,
        "importance": info["importance"],
        "clinical_meaning": clinical_why,
        "early_warning": info["early_warning"],
        "diet_actions": info["how_to_control"]["diet_actions"],
        "recommended_fruits": info["how_to_control"]["recommended_fruits"],
        "exercises": info["how_to_control"]["exercises"],
        "daily_precautions": info["how_to_control"]["daily_precautions"]
    }
