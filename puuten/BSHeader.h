//
//  BSHeader.h
//  puuten
//
//  Created by wang jialei on 12-8-3.
//
//

#import <UIKit/UIKit.h>

@interface BSHeader : UIView
@property (assign, nonatomic) int bs_id;
@property (assign, nonatomic) NSString *name;
@property (assign, nonatomic) NSString *avatar_url;
@property (strong, nonatomic) UILabel *nameLabel;
@property (strong, nonatomic) UIImageView *imageView;

@end
