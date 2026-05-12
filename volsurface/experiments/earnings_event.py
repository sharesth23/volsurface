def vol_surface_shifts(pre_event_surface, post_event_surface, strikes, maturities):
    shifts = {}

    for K in strikes:
        for T in maturities:
            shift = post_event_surface.iv(K, T) - pre_event_surface.iv(K, T)
            shifts[(K, T)] = shift

    return shifts
