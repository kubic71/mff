# How will the probability estimation that the door is open evolve over time?

# z[0] = p(sensor positive | door is open)

class Sensor:
    def __init__(self, positive_given_open, positive_given_closed):
        # p(sensor positive | door is open)
        self.positive_given_open = positive_given_open
        self.negative_given_open = 1 - positive_given_open

        # p(sensor positive | door is closed)
        self.positive_given_closed = positive_given_closed
        self.negative_given_closed = 1 - positive_given_closed

    def update_estimate_measurement_positive(self, prior_door_open: float) -> float:
        # how will the probability estimation change, given positive measurement?

        # new_estimate = likelihood * prior_door_open / evidence

        likelihood = self.positive_given_open
        p_evidence = self.positive_given_open * prior_door_open + self.positive_given_closed * (1 - prior_door_open)

        return likelihood * prior_door_open / p_evidence

    def update_estimate_measurement_negative(self, prior_door_open: float) -> float:
        # how will the probability estimation change, given negative measurement?

        # new_estimate = likelihood * prior_door_open / evidence

        likelihood = self.negative_given_open
        p_evidence = self.negative_given_open * prior_door_open + self.negative_given_closed * (1 - prior_door_open)

        return likelihood * prior_door_open / p_evidence




z1_sensor = Sensor(0.6, 0.3)
z2_sensor = Sensor(0.5, 0.6)

prior_door_open = 0.5

p_z1 = z1_sensor.update_estimate_measurement_positive(prior_door_open)
print(f"p(open | z1) = {p_z1}")

p_z1_z2 = z2_sensor.update_estimate_measurement_positive(p_z1)
print(f"p(open | z1, z2) = {p_z1_z2}")


print("\n\n\n\n")


def evolve_sequence(sequence):
    estimate = 0.5

    for measurement in sequence:
        if measurement == "z1_open":
            new_estimate = z1_sensor.update_estimate_measurement_positive(estimate)
        elif measurement == "z1_closed":
            new_estimate = z1_sensor.update_estimate_measurement_negative(estimate)
        elif measurement == "z2_open":
            new_estimate = z2_sensor.update_estimate_measurement_positive(estimate)
        elif measurement == "z2_closed":
            new_estimate = z2_sensor.update_estimate_measurement_negative(estimate)

        print(f"{measurement}: {estimate} -> {new_estimate}")
        estimate = new_estimate

# z1: open
# z1: open
# z2: closed
# z2: open
# z2: open
# z1: open
# z1: closed
evolve_sequence(["z1_open", "z1_open", "z2_closed", "z2_open", "z2_open", "z1_open", "z1_closed"])

print("\n\n\nCompare with, if we first get all z_1 measurement and then all z_2 measurements:")
evolve_sequence(["z1_open", "z1_open", "z1_open", "z1_closed", "z2_closed", "z2_open", "z2_open"])


print("\n\n\nCompare it with the case as if the z2 always reported 'closed' with the same readout order.")
evolve_sequence(["z1_open", "z1_open", "z2_closed", "z2_closed", "z2_closed", "z1_open", "z1_closed"])


